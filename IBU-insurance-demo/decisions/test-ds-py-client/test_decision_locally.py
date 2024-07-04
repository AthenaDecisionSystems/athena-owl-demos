import re
import json
import requests

from ComplaintHandling_generated_model import Request, Claim, InsurancePolicy, PolicyType, SubType, Client, ComplaintOnClaim, Status, ClientInteraction, Motive

DATA_APIS_URL = 'http://localhost:8080/repository'
DS_URL = 'http://localhost:9060/DecisionService/rest/v1/ComplaintHandling/1.0/nextBestAction'

"""
workbook = CalamineWorkbook.from_path("data/decision-refdata.xlsx")
worksheet = workbook.get_sheet_by_name("Explanations").to_python()
headers, *data_rows = worksheet
"""

def getInputPayload(scenario: str) -> str:
    """Read JSON from file, check it is a valid JSON and return corresponding string"""
    f = open(scenario + ".json")
    json_data = json.load(f)
    assert len(json_data["complaint"]) > 0  # the client object should contain multiple keys
    return json.dumps(json_data)


def callDecisionService(payload: str):
    response = requests.post(
        DS_URL,
        data=payload,
        headers={"Content-Type": "application/json"}
    )
    return response

def callDataAPI(path: str) -> str:
    response = requests.get(
        f'{DATA_APIS_URL}/{path}'
    )
    return response

def test_decision_service_with_predefined_payload():
    # in this test, we call the ODM decision service using a predefined payload
    payload: str = getInputPayload("scenario - leger retard")
    response = callDecisionService(payload)
    assert response.status_code == 200
    details = response.json()["response"]
    # print(details)
    actions = details['actions']
    assert len(actions) == 3
    assert actions[0]["typeDisc__"] == "Discount"
    assert actions[0]["explanationCode"] == "AC-AUTO-SUBV-DISC"
    missingInfoElements = details['missingInfoElements']
    assert len(missingInfoElements) == 0

def test_decision_service_with_pydantic():
    request = Request(complaint= 
                      ComplaintOnClaim(
                          claim=Claim(
                              policy=InsurancePolicy(
                                  policyType=PolicyType.Auto,
                                  subType=SubType.AutoThirdParty,
                                  client = Client(
                                      firstName = "Joe",
                                      lastName = "Smith",
                                      cltvPercentile=56,
                                      propensityToUpgradePolicy=0.34
                                  ),
                                  coverages = [],
                                  options=[]
                              ),
                              status=Status.IN_PROCESS_VERIFIED,
                              creationDate="2024-04-05",
                              damages=[],
                              settlementOffer=None
                          ),
                          interactions=[
                              ClientInteraction(
                                  date="2024-04-15",
                                  motive=Motive.UnsatisfiedWithAppliedCoverages,
                                  intentionToLeave=False
                              )
                          ]))
    
    # Serialize input payload
    request_str: str = request.model_dump_json()

    with open("pydantic_payload.json", "w") as text_file:
        text_file.write(request_str)

    response = callDecisionService(request_str)
    assert response.status_code == 200

    details = response.json()["response"]
    # print(details)
    with open("ds_response.json", "w") as text_file:
        text_file.write(json.dumps(response.json()))

    actions = details['actions']
    assert len(actions) == 1
    assert actions[0]["typeDisc__"] == "Discount"

    missingInfoElements = details['missingInfoElements']
    assert len(missingInfoElements) == 0

def test_decision_service_with_claim_2():
    # in this test, we call the ODM decision service by passing a payload with two parts:
    # - a claim obtained from our data API that loads it from Postgres
    # - a list of interactions that we create programmatically

    # these 3 data elements come from the chat
    claim_id = 2
    motive = Motive.UnsatisfiedWithAppliedCoverages
    intentionToLeave = False
    intentionToLeaveStr = str(intentionToLeave).lower()
    response = callDataAPI(f'claims/{claim_id}')
    assert response.status_code == 200
    claim_json = response.json()
#    claim_json_str = """{"id":1,"status":"IN_PROCESS_VERIFIED","creationDate":"2024-02-21T23:00:00.000+00:00","targetDurationInDays":21,"policy":{"id":1,"effectiveDate":"2023-06-05T22:00:00.000+00:00","expirationDate":"2024-06-05T22:00:00.000+00:00","policyType":"Standard","client":{"id":1,"firstName":"Jane","lastName":"Dupont","dateOfBirth":"1967-02-21T23:00:00.000+00:00","paymentScore":3,"claimsScore":3,"preferredChannel":"email","vip":true},"coverages":[]},"damages":[],"settlementOffer":null}"""
#    assert claim_json_str == json.dumps(claim_json, separators=(',', ':'))

    payload = f"""
    {{
      "complaint": {{
        "claim": {json.dumps(claim_json)},
        "interactions": [
                {{
                    "date": "2024-09-14",
                    "motive": "{motive.value}",
                    "intentionToLeave": {intentionToLeaveStr}
                }}
        ]      
      }}
    }}
    """

    with open("fetched_payload.json", "w") as text_file:
        text_file.write(payload)

    response = callDecisionService(payload)
    assert response.status_code == 200

    details = response.json()["response"]
    print(details)

    actions = details['actions']
    assert len(actions) == 2
    assert actions[0]["typeDisc__"] == "SimpleUpsellProposal"
    assert actions[1]["typeDisc__"] == "Voucher"

    missingInfoElements = details['missingInfoElements']
    assert len(missingInfoElements) == 0

def test_get_claims_1():
    response = callDataAPI('claims/1')
    assert response.status_code == 200
    claim_json = response.json()
    policy = claim_json['policy']
    assert policy != None
    damages = claim_json['damages']
    assert len(damages) == 1
    assert claim_json['status'] == 'IN_PROCESS_VERIFIED'

def test_get_claims_2():
    response = callDataAPI('claims/2')
    assert response.status_code == 200
    claim_json = response.json()
    print(claim_json)
    policy = claim_json['policy']
    assert policy != None
    damages = claim_json['damages']
    assert len(damages) == 2
    assert claim_json['status'] == 'IN_PROCESS_VERIFIED'

if __name__ == '__main__':
    # test_get_claims_2()
    test_decision_service_with_claim_2()