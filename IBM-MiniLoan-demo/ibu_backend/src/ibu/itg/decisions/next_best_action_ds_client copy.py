"""
Copyright 2024 Athena Decision Systems
@author Jerome Boyer
"""

import requests, logging, json

#from athena.glossary.glossary_mgr import build_get_glossary, Glossary

from ibu.itg.ds.loanapp_client_repo_mock import BorrowerRepositoryInMem
from ibu.itg.ds.pydantic_generated_model import Request, Borrower, LoanRequest

from string import Template

LOGGER = logging.getLogger(__name__)

DS_URL = 'http://localhost:9060/DecisionService/rest/v1/production_deployment/1.0/loan_validation_production'

def _get_borrower_data(config, first_name: str, last_name: str):
    borrower_repository= BorrowerRepositoryInMem.initialize_client_db()
    borrower = borrower_repository.get_client_by_name(first_name, last_name)
    return borrower


def _prepare_odm_payload(borrower, loanRequest):
    request = Request(loan=loanRequest, borrower=borrower)

     # Serialize input payload
    request_str: str = request.model_dump_json()

    with open("pydantic_payload.json", "w") as text_file:
        text_file.write(request_str)

    return request_str

def callRuleExecutionServer(payload: str):
    response = requests.post(
        DS_URL, #change using config data
        payload,
        headers={"Content-Type": "application/json"}
    )
    return response

def _process_odm_response(odm_resp : str , glossary: Glossary, locale: str):
    pass

#def callDecisionService(config, client_repo, first_name: str, last_name: str, locale: str = "en"):
def callDecisionService(first_name: str, last_name: str):
    borrower =  _get_borrower_data(first_name, last_name)

    loanRequest=LoanRequest(
        numberOfMonthlyPayments= 12,
        startDate = "2006-08-19T19:27:14.000+0200",
        amount = 100000,
        loanToValue= 0.7
                      )
    payload = _prepare_odm_payload(borrower, loanRequest)

    response = callDecisionService(payload)
    assert response.status_code == 200

    #details = response.json()["response"]
    # print(details)
    with open("ds_response.json", "w") as text_file:
        text_file.write(json.dumps(response.json()))

    response_json = response.json()
    print(response_json)

'''
    json_data = {}  # ADD payload prep here
    LOGGER.debug(f"\n\n {json_data}")
    #print(type(json_data))
    response = requests.post(
        config.owl_best_action_ds_url,
        data=json.dumps(json_data),
        headers={"Content-Type": "application/json"}
    )
    if response.status_code == 200:
        if response.json()["response"] != None:
            g = build_get_glossary(config.owl_glossary_path) # should be loaded one time 
            final_response= _process_odm_response(response.json()["response"], g, locale)
            return final_response
    else:
        LOGGER.error("** Error during decision service call:", response)
        return "Error during decision service call"
   ''' 

