"""
Copyright 2024 Athena Decision Systems
@author Jerome Boyer
"""
from langchain.agents import tool
from langchain.tools.retriever import create_retriever_tool
from ibu.itg.ds.ComplaintHandling_generated_model import Motive
from importlib import import_module
from typing import Sequence, Any
import logging
from athena.app_settings import get_config
from athena.routers.dto_models import ConversationControl
from athena.itg.store.content_mgr import get_content_mgr
from ibu.itg.decisions.next_best_action_ds_client import callDecisionService

"""
Tool manager manages the different tools to be used by the different Agents of the solution.
It has dependencies and knowledge on the domain of the solution.
Use decision service, content manager and different repository
"""

# For each tool definition, the function signature is important as it will be what LLM will try
# to build for
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
        LOGGER.debug("Created repository for client")
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
        LOGGER.debug("Created repository for claim")
    return _insurance_claim

@tool
def get_client_by_id(id: int) -> dict:
    """get insurance client information given its unique client identifier id"""
    return build_or_get_insurance_client_repo().get_client_json(id)

@tool
def get_claim_by_id(id: int) -> dict:
    """get insurance claim information given its unique claim identifier id"""
    return build_or_get_instantiate_claim_repo().get_claim_json(id)

@tool
def get_client_by_name(name: str) -> dict:
    """get client information given his or her name"""
    return build_or_get_insurance_client_repo().get_client_by_name(name)

@tool
def define_next_best_action_with_decision(claim_id : int, client_motive: Motive, intentionToLeave: bool ):
    """perform the next best action given the current state of the insurance claim knowing 
    its unique claim_id and the current client motivation.
    extract the  client motive and if he has the intention to leave
    """
    config = get_config()
    return callDecisionService(config, build_or_get_instantiate_claim_repo(), claim_id, client_motive, intentionToLeave, "en")




_tools = [get_client_by_id, get_claim_by_id, get_client_by_name]

def get_tools_to_use(conversationControl:ConversationControl) -> Sequence[Any] :
    """
    Define the Tools to be used by the Agent. It is controlled by the input controller object to give
    more context
    """
    _tools = [get_client_by_id, get_claim_by_id]
    if conversationControl.callWithDecisionService:
        _tools.append(define_next_best_action_with_decision)
    if conversationControl.callWithVectorStore:
        retriever = get_content_mgr().get_retriever()
        retriever_tool = create_retriever_tool(retriever, "insurance_specific",
                            "Search for information about insurance policy. For any questions about insurance, you must use this tool!")
        _tools.append(retriever_tool)
    LOGGER.debug(_tools)
    return _tools

def get_current_tools():
    return _tools