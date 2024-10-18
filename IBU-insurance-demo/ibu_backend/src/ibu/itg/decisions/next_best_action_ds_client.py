"""
Copyright 2024 Athena Decision Systems
@author Jerome Boyer
"""
import os
from typing import Optional

import requests, logging, json
from importlib import import_module

try:
    mode = "DEV"
    from ibu_backend.src.ibu.itg.ds.ComplaintHandling_generated_model import *
    from ibu_backend.src.ibu.app_settings import get_config
    from ibu_backend.src.ibu.itg.decisions.decision_center_extraction import DecisionCenterExtract
    from ibu_backend.src.ibu.itg.decisions.decision_service_traceability import set_trace
    from ibu_backend.src.ibu.itg.decisions.e2e_decision_explainability import ExplanationArtefactList
except ImportError:
    mode = "PACK"
    from ibu.itg.ds.ComplaintHandling_generated_model import *
    from ibu.app_settings import get_config
    from ibu.itg.decisions.decision_center_extraction import DecisionCenterExtract
    from ibu.itg.decisions.decision_service_traceability import set_trace
    from ibu.itg.decisions.e2e_decision_explainability import ExplanationArtefactList
    from athena.glossary.glossary_mgr import build_get_glossary

from fastapi.encoders import jsonable_encoder
from string import Template


logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')
LOGGER = logging.getLogger(__name__)
if get_config().logging_level == "DEBUG":
    LOGGER.setLevel(logging.DEBUG)

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S')
LOGGER = logging.getLogger(__name__)


def _instantiate_claim_repo(config):
    """
    From the configuration loaded, instantiate the class for the claim repository
    """
    module_path, class_name = config.app_insurance_claim_repository.rsplit('.', 1)
    mod = import_module(module_path)
    klass = getattr(mod, class_name)
    return klass(config)


def _get_claim_data(config, claim_id: int):
    app_insurance_claim_repository = _instantiate_claim_repo(config)
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


def _process_odm_response(decision_center_extract: Optional[DecisionCenterExtract],
                          json_response: dict,
                          g: build_get_glossary,
                          locale: str) -> str:
    """Handles the response from the ODM decision service by formatting it in a way that the LLM can interpret.

    Sample response:
            {
              "actions": [
                {
                  "typeDisc__": "SimpleUpsellProposal",
                  "explanationCode": "AC-HOME-CONT-UP",
                  "description": "upgrade of the policy to include contents coverage"
                },
                {
                  "typeDisc__": "Voucher",
                  "explanationCode": "AC-HOME-CONT-VOUCHER",
                  "description": "Voucher to spend with affiliate provider",
                  "value": 200.0
                }
              ],
              "missingInfoElements": [],
              "outputTraces": [],
              "explanation": [
                {
                  "name": "Complaint Handling.Applied coverages.Targeted.Home.AC-HOME-CONT-UP - Upgrade policy to include content",
                  "type_": "RULE",
                  "html": "<span><font color=\"#000080\"><b><i>if</i></b></font><br>&nbsp;&nbsp;&nbsp;the subtype of <font color=\"...",
                  "documentation": "EXPLANATION\n# Upsell rule (AC-HOME-CONT-UP)\nAn upsell to the home policy should be proposed ...\nEND OF EXPLANATION  \nEXPLANATION FORMAT: md"
                },
                {
                  "name": "Complaint Handling.Applied coverages.Targeted.Home.AC-HOME-CONT-VOUCHER - Propose voucher for extra service with affiliate provider",
                  "type_": "RULE",
                  "html": "<span><font color=\"#000080\"><b><i>if</i></b></font><br>&nbsp;&nbsp;&nbsp;the subtype of <font color=\"...",
                  "documentation": "EXPLANATION\n# Voucher rule (AC-HOME-CONT-VOUCHER)\nA voucher should be offered to customers  ...\nEND OF EXPLANATION  \nEXPLANATION FORMAT: md"
                }
              ]
            }
    """
    LOGGER.info(f"@@@@_process_odm_response> ODM response:")
    LOGGER.info(f"\n\n {json.dumps(json_response, indent=4)}")

    response2 = json_response["response"]
    response2["explanation"] = []

    if decision_center_extract:
        eal: ExplanationArtefactList = ExplanationArtefactList.build(decision_center_extract, json_response)
        if eal.errors_and_warnings:
            for e in eal.errors_and_warnings:
                LOGGER.error(e)
        for artefact in eal.explanation_artefacts:
            LOGGER.info("artefact.documentation.content:")
            LOGGER.info(artefact.documentation.content)
            response2["explanation"].append(artefact.dict())

    if len(response2) == 0:
        return g.get_phrase("NoAction", locale)
    else:
        result = "\n\nThe analysis of the customer situation leads to these retention actions:\n\n"

        for key in response2.keys():
            value = response2[key]
            if key == "actions":
                for action in value:
                    result += f"- {_format_action(g, action, locale)}\n"
            else:
                logging.debug(f"** Ignoring key: {key}")

        if decision_center_extract:
            eal: ExplanationArtefactList = ExplanationArtefactList.build(decision_center_extract, json_response)
            result = result + "\n" + "<explanation>"
            for artefact in eal.explanation_artefacts:
                result = result + "\n\n" + artefact.documentation.content + "\n-----\n"
            result = result + "\n\n" + "</explanation>"

        if decision_center_extract:
            eal: ExplanationArtefactList = ExplanationArtefactList.build(decision_center_extract, json_response)
            result = result + "\n" + "<rule>"
            for artefact in eal.explanation_artefacts:
                parts = artefact.name.split('.')
                result =  result + "\n\n" + "<h4>" + parts[-1] + "</h4><br/>" + artefact.html + "<hr/>"
            result = result + "\n\n" + "</rule>"

        logging.info(f"_process_odm_response> ODM response with explanation:")
        logging.info(result)
        logging.info(f"*"*50)

        return result


def callDecisionServiceWithClaim(config, 
                                 claim: Claim, 
                                 client_motive: Motive, 
                                 intentionToLeave: bool,
                                 locale: str = "en"):

    payload = _prepare_odm_payload(claim, client_motive, intentionToLeave)

    try:
        decision_center_extract = DecisionCenterExtract.read_from_file('./decisions/ds-insurance-pc-claims-nba.json')
    except Exception as e:
        LOGGER.error(f"callDecisionService> An error occurred: {e}")
        LOGGER.error(f"callDecisionService> Rule traceability will be disabled")
        decision_center_extract = None
        
    if decision_center_extract:
        set_trace(payload, True)

    json_data = jsonable_encoder(payload)
    LOGGER.debug(f"\n\ncallDecisionService>/n {json_data}")
    LOGGER.debug(f"\n\ncallDecisionService>/n {json.dumps(json_data, indent=4)}")
    response = requests.post(
        config.owl_best_action_ds_url,
        data=json.dumps(json_data),
        headers={"Content-Type": "application/json"}
    )

    if response.status_code == 200:
        json_response = response.json()
        json_response2 = json_response["response"]

        if json_response2 is not None:
            g = build_get_glossary(config.owl_glossary_path)  # should be loaded one time
            final_response = _process_odm_response(decision_center_extract, json_response, g, locale)
            LOGGER.info("callDecisionService> final_response")
            LOGGER.info(final_response)
            LOGGER.info(f"\n\ncallDecisionService> After post processing:")
            LOGGER.info(f"\n\n{json.dumps(json_response2, indent=4)}")
            return final_response
        else:
            LOGGER.error("callDecisionService> ** Decision service call does not return a response:", response)
            return "** Decision service call does not return a response"
    else:
        LOGGER.error("callDecisionService> ** Error during decision service call:", response)
        return "Error during decision service call"
    
    
def callDecisionService(config, 
                        claim_repo, 
                        claim_id: int, 
                        client_motive: Motive, 
                        intentionToLeave: bool,
                        locale: str = "en"):
    """
    Delegate the next best action to an external decision service
    """
    LOGGER.info(f"\n\n callingDecisionService")

    claim = claim_repo.get_claim(claim_id).model_dump()
    return callDecisionServiceWithClaim(config, claim, client_motive, intentionToLeave, locale)


def callDecisionServiceMock(config, claim_repo, claim_id: int, client_motive: Motive, intentionToLeave: bool,
                            locale: str = "en"):
    """Mock function to support unit tests. This is injected via config.yaml with the parameter: owl_agent_decision_service_fct_name"""
    rep = Response()
    rep.actions = [Action(explanationCode="Propose a Vousher for 100$", typeDisc__="")]
    return rep