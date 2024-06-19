import logging
from athena.app_settings import get_config
from importlib import import_module
from langchain.tools import BaseTool, StructuredTool
from ibu.itg.decisions.next_best_action_ds_client import callDecisionService
from ibu.itg.ds.ComplaintHandling_generated_model import Motive
LOGGER = logging.getLogger(__name__)

_insurance_claim = None

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



def get_claim_by_id(id: int) -> dict:
    """get insurance claim information given its unique claim identifier id"""
    return build_or_get_instantiate_claim_repo().get_claim_json(id)

def define_next_best_action_with_decision(claim_id : int, client_motive: Motive, intentionToLeave: bool ):
    """perform the next best action given the current state of the insurance claim knowing 
    its unique claim_id and the current client motivation.
    extract the  client motive and if he has the intention to leave
    """
    config = get_config()
    return callDecisionService(config, build_or_get_instantiate_claim_repo(), claim_id, client_motive, intentionToLeave, "en")

methods = {"get_claim_by_id" : get_claim_by_id, "define_next_best_action_with_decision": define_next_best_action_with_decision}

def define_tool(name: str, description: str, funct_name):
    return StructuredTool.from_function(
        func=methods[funct_name],
        name=funct_name,
        description=description,
        #args_schema=,
        return_direct=False,
    )