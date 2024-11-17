"""
Copyright 2024 Athena Decision Systems
@author Jerome Boyer
"""
import logging
from typing import Optional, Any
from importlib import import_module
from langchain.tools import StructuredTool, Tool
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.tools.retriever import create_retriever_tool

from ibu.app_settings import get_config
from athena.llm.tools.tool_mgr import DefaultToolInstanceFactory
from athena.itg.store.content_mgr import get_content_mgr

from ibu.itg.decisions.next_best_action_ds_client import callDecisionService, callDecisionServiceMock
from ibu.itg.ds.ComplaintHandling_generated_model import Motive, Status, Claim


LOGGER = logging.getLogger(__name__)

_insurance_client = None
_insurance_claim = None

def build_or_get_insurance_client_repo():
    global _insurance_client
    if _insurance_client == None:
        config = get_config()
        module_path, class_name = config.app_insurance_client_repository.rsplit('.',1)
        mod = import_module(module_path)
        klass = getattr(mod, class_name)
        LOGGER.debug(f"---> klass {klass}")
        _insurance_client= klass(config)
        LOGGER.info(f"Created repository for client using {config.app_insurance_client_repository}")
    return _insurance_client

def build_or_get_instantiate_claim_repo():
    """
    From the configuration loaded, instantiate the class for the claim repository
    """
    global _insurance_claim
    if _insurance_claim == None:
        config = get_config()
        module_path, class_name = config.app_insurance_claim_repository.rsplit('.',1)
        mod = import_module(module_path)
        klass = getattr(mod, class_name)
        _insurance_claim= klass(config)
        LOGGER.info(f"Created repository for claim using {config.app_insurance_claim_repository}")
    return _insurance_claim


# ============================================= Function / Tool  Definitions ======================== 

def get_client_by_id(id: int) -> dict:
    """get insurance client information given its unique client identifier id"""
    LOGGER.debug(f"Call service get_client_by_id: id= {id}")
    result = build_or_get_insurance_client_repo().get_client_json(id)
    if result == None:
        return {"error": f"Error: client {id} not found"}
    return result

def get_client_by_name(firstname: str, lastname: str) -> dict:
    """get customer details given his or her last name and first name"""
    return build_or_get_insurance_client_repo().get_client_by_name(firstname, lastname)

def get_claim_by_id(id: int) -> dict:
    """get insurance claim details given its unique claim identifier id or number"""
    LOGGER.debug(f"Call service get_claim_by_id: id= {id}")
    result=build_or_get_instantiate_claim_repo().get_claim_json(id)
    if result == None:
        return {"error": f"Error: claim {id} not found"}
    return result

def define_next_best_action_with_decision(claim_id : int, client_motive: Motive, intentionToLeave: bool ):
    """
    This is a decision service that provides recommendation based on the company's policies.
    You input the customer's motivation, risk of churn and the claim_id. You get actions to be taken and business rule's reference.
    """
    LOGGER.debug(f"Call Decision Service: claim_id {claim_id} client_motive {client_motive} intentionToLeave {intentionToLeave}")
    config = get_config()
    result = callDecisionService(config, build_or_get_instantiate_claim_repo(), claim_id, client_motive, intentionToLeave, "en")
    return result


def get_claim_status_by_user_name(firstname: str, lastname: str):
    """
    """
    client = build_or_get_insurance_client_repo().get_client_by_name(firstname, lastname)
    claims = build_or_get_instantiate_claim_repo().get_all_claims()
    for claim in claims:
        if type(claim) == dict:
            aClaim=Claim.model_validate(claim)
        else:
            aClaim=claim
        if aClaim.policy and aClaim.policy.client and aClaim.policy.client.id == client.id:
            return aClaim.status
    return None


def search_corpus(query: str):
    LOGGER.info(f"/// search_corpus with query: {query}")
    content_mgt= get_content_mgr()
    LOGGER.info(f"/// owl_agent_content_collection_name: {get_config().owl_agent_content_collection_name}")
    return content_mgt.search(get_config().owl_agent_content_collection_name, query,1)

        
class IbuInsuranceToolInstanceFactory(DefaultToolInstanceFactory):
    methods = {
        "get_client_by_id" : get_client_by_id, 
        "get_client_by_name": get_client_by_name, 
        "get_claim_by_id" : get_claim_by_id, 
        "get_claim_status_by_user_name": get_claim_status_by_user_name,
        "define_next_best_action_with_decision": define_next_best_action_with_decision,
        "search_corpus": search_corpus
        }
