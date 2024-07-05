import logging
from typing import Optional, Any
from importlib import import_module
from langchain.tools import StructuredTool
from langchain_community.tools.tavily_search import TavilySearchResults


from athena.app_settings import get_config
from athena.llm.tools.tool_factory import ToolInstanceFactoryInterface, OwlToolEntity

from ibu.itg.decisions.next_best_action_ds_client import callDecisionService
from ibu.itg.ds.ComplaintHandling_generated_model import Motive


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
        _insurance_client= klass()
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
        _insurance_claim= klass()
        LOGGER.debug("Created repository for claim")
    return _insurance_claim

def get_client_by_id(id: int) -> dict:
    """get insurance client information given its unique client identifier id"""
    return build_or_get_insurance_client_repo().get_client_json(id)

def get_client_by_name(name: str) -> dict:
    """get client information given his or her name"""
    return build_or_get_insurance_client_repo().get_client_by_name(name)

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



methods = {"get_client_by_id" : get_client_by_id, 
           "get_client_by_name": get_client_by_name, 
            "get_claim_by_id" : get_claim_by_id, 
            "define_next_best_action_with_decision": define_next_best_action_with_decision}

def define_tool(description: str, funct_name, args: Optional[str]):
    if args:
        return StructuredTool.from_function(
            func=methods[funct_name],
            name=funct_name,
            description=description,
            args_schema= arg_schemas[args], # type: ignore
            return_direct=False,
        )
    else:
        return StructuredTool.from_function(
            func=methods[funct_name],
            name=funct_name,
            description=description,
            return_direct=False,
        )
        
class IbuInsuranceToolInstanceFactory(ToolInstanceFactoryInterface):
    
    def build_tool_instances(self, tool_entities: list[OwlToolEntity]) -> list[Any]:
        tool_list=[]
        for tool_entity in tool_entities:
            if tool_entity.tool_id == "tavily":
                tool_list.append(TavilySearchResults(max_results=2))
            elif tool_entity.tool_fct_name in methods.keys():
                tool_list.append(define_tool( tool_entity.tool_description, tool_entity.tool_fct_name, tool_entity.tool_arg_schema_class))# type: ignore
            else:
                raise Exception(f"{tool_entity.tool_id} Not yet implemented")
        return tool_list