
import json
import requests

#from ComplaintHandling_generated_model import Request, Claim, InsurancePolicy, PolicyType, SubType, Client, ComplaintOnClaim, Status, ClientInteraction, Motive

#DATA_APIS_URL = 'http://localhost:8080/repository'
DS_URL = 'http://localhost:9060/DecisionService/rest/v1/production_deployment/1.0/loan_validation_production'



def callDecisionService(payload: str):

    response = requests.post(
        DS_URL,
        payload,
        headers={"Content-Type": "application/json"}
    )
    return response

#payload: str = getInputPayload("scenario - pipe clean")

def test_decision_service_with_predefined_payload():
    #payload: str = getInputPayload("scenario - pipe clean")
    mypayload = """{
    "loan": {
        "numberOfMonthlyPayments": 3,
        "startDate": "2006-08-19T19:27:14.000+0200",
        "amount": 3,
        "loanToValue": 10517320
    },
    "__DecisionID__": "string",
    "borrower": {
        "firstName": "string",
        "lastName": "string",
        "birth": "2008-09-29T03:49:45.000+0200",
        "SSN": {
        "areaNumber": "string",
        "groupCode": "string",
        "serialNumber": "string"
        },
        "yearlyIncome": 3,
        "zipCode": "string",
        "creditScore": 3,
        "spouse": {
        "birth": "2024-06-21T08:17:15.423+0200",
        "SSN": {
            "areaNumber": "",
            "groupCode": "",
            "serialNumber": ""
        },
        "yearlyIncome": 0,
        "creditScore": 0,
        "latestBankruptcy": {
            "chapter": 0
        }
        },
        "latestBankruptcy": {
        "date": "2014-09-19T01:18:33.000+0200",
        "chapter": 3,
        "reason": "string"
        }
    }
    }"""
    response = callDecisionService(mypayload)
        # Print the response
    response_json = response.json()
    print(response_json)
    #print(response)


print(test_decision_service_with_predefined_payload())