"""
Copyright 2024 Athena Decision Systems
@author Jerome Boyer
"""

import requests, logging, json
from importlib import import_module
from ibu.itg.ds.ComplaintHandling_generated_model import *
from fastapi.encoders import jsonable_encoder
from athena.glossary.glossary_mgr import build_get_glossary
from string import Template

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S')
LOGGER = logging.getLogger(__name__)


    
def _instantiate_claim_repo(config):
    """
    From the configuration loaded, instantiate the class for the claim repository
    """
    module_path, class_name = config.app_insurance_claim_repository.rsplit('.',1)
    mod = import_module(module_path)
    klass = getattr(mod, class_name)
    return klass(config)

def _get_claim_data(config, claim_id: int):
    app_insurance_claim_repository= _instantiate_claim_repo(config)
    claim = app_insurance_claim_repository.get_claim(claim_id)
    return claim

def _prepare_odm_payload(claim, motive: Motive, intentionToLeave: bool):
    data = {
        "complaint": {
            "claim": claim,
            "interactions": [
                {
                    "date": "2024-04-15T00:00:00",
                    "motive": motive.name,
                    "intentionToLeave": intentionToLeave,
                }
            ]
        }
    }
    LOGGER.debug(f"@@@>  {data}")
    return data

def _format_action(g: build_get_glossary, action: dict, locale: str = "en") -> str:
    """Formats the action string for display.

    Sample action:
    {'typeDisc__': 'CommunicateWithClient', 
    'explanationCode': 'AC-AUTO-TPL-5', 
    'channel': 'email', 
    'messageType': 'Proposal'
    }

    """
    action_type = action["typeDisc__"]
    if action_type == "CommunicateWithClient":
        t = Template(g.get_phrase("CommunicateWithClient", locale))
        return t.substitute(
            channel=g.get_phrase(action["channel"], locale),
            messageType=g.get_phrase(action["messageType"], locale),
        )
    elif action_type == "PrepareProposal":
        return g.get_phrase("PrepareProposal", locale)
    elif action_type == "ResendTo":
        t = Template(g.get_phrase("ResendTo", locale))
        return t.substitute(recipient=g.get_phrase(action["recipient"], locale))
    elif action_type == "CommercialEffort":
        return g.get_phrase("CommercialEffort", locale)
    elif action_type == "SimpleUpsellProposal":
        t = Template(g.get_phrase("SimpleUpsellProposal", locale))
        return t.substitute(description=action["description"])
    elif action_type == "Voucher":
        return g.get_phrase(action["explanationCode"], locale)
    else:
        t = Template(g.get_phrase("UnknownAction", locale))
        return t.substitute(actionType=action_type)
    
def _process_odm_response(resp_json, g: build_get_glossary, locale: str):
    """Handles the response from the ODM decision service by formatting it in a way that the LLM can interpret.

    Sample response:
            {'actions': [{'typeDisc__': 'CommunicateWithClient', 
                        'explanationCode': 'AC-AUTO-TPL-5', 
                        'channel': 'email', 
                        'messageType': 'Proposal'
                        }, 
                        {'typeDisc__': 'Reassign', 
                        'explanationCode': 'AC-AUTO-TPL-5', 
                        'recipient': 'SpecializedClientRepresentative', 
                        'suggestion': None}
                        ], 
            'missingInfoElements': [], 
            'outputTraces': []}}

    """

    LOGGER.debug(f"@@@> ODM response:  {resp_json}")
    if len(resp_json) == 0:
        return g.get_phrase("NoAction", locale)
    else:
        result = g.get_phrase("analysis_gives", locale)
        for key in resp_json.keys():
            value = resp_json[key]
            if key == "actions":
                result += f"{g.get_phrase('Actions', locale)}:\n"
                i = 1
                for action in value:
                    result += f"{i}.{_format_action(g,action, locale)}\n"
                    i += 1
            else:
                logging.debug(f"** Ignoring key: {key}")
        return result


def callDecisionService(config, claim_repo, claim_id: int, client_motive: Motive, intentionToLeave: bool, locale: str = "en"):
    """
    Delegate the next best action to an external decision service
    """
    claim =  claim_repo.get_claim(claim_id).model_dump()
    payload = _prepare_odm_payload(claim, client_motive, intentionToLeave)
    json_data = jsonable_encoder(payload)
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
    

def callDecisionServiceMock(config, claim_repo, claim_id: int, client_motive: Motive, intentionToLeave: bool, locale: str = "en"):
    """Mock function to support unit tests. This is injected via config.yaml with the parameter: owl_agent_decision_service_fct_name"""
    rep = Response()
    rep.actions=[Action(explanationCode="Propose a Vousher for 100$", typeDisc__= "")]
    return rep