import logging, uuid, datetime
from ibu.app_settings import get_config
from importlib import import_module
from typing import Optional, Any
from pydantic import BaseModel, Field
from langchain.tools import StructuredTool
from ibu.itg.ds.loanapp_borrower_repo_mock import LoanApplicationClientRepositoryInterface
from ibu.itg.ds.pydantic_generated_model import LoanRequest, Request
from ibu.itg.decisions.next_best_action_ds_client import callRuleExecutionServer
from athena.llm.tools.tool_mgr import OwlToolEntity
from athena.llm.tools.tool_factory import ToolInstanceFactoryInterface, OwlToolEntity
from langchain_community.tools.tavily_search import TavilySearchResults
LOGGER = logging.getLogger(__name__)

_loan_client: LoanApplicationClientRepositoryInterface = None

def build_or_get_loan_client_repo() -> LoanApplicationClientRepositoryInterface:
    global _loan_client
    if not _loan_client:
        config = get_config()
        module_path, class_name = config.app_borrower_repository.rsplit('.',1)
        mod = import_module(module_path)
        klass = getattr(mod, class_name)
        LOGGER.debug(f"---> klass {klass}")
        _loan_client= klass()
        LOGGER.debug("Created repository for client")
    return _loan_client



def get_client_by_name(first_name: str, last_name: str) -> str | None:
    """get borrower client information given his or her name"""
    return build_or_get_loan_client_repo().get_client_by_name_json(first_name,last_name)

def define_next_best_action_with_decision(loanRequest: LoanRequest, first_name: str, last_name: str ):
    """perform the loan application request assessment for the given borrower name
    """
    if loanRequest and type(loanRequest) == LoanRequest:
        borrower =  build_or_get_loan_client_repo().get_client_by_name(first_name=first_name, last_name=last_name)
        ds_request = Request(__DecisionID__= str(uuid.uuid4),borrower=borrower, loan=loanRequest)
        payload: str = ds_request.model_dump_json()
        return callRuleExecutionServer(payload)
    else:
        return None

def assess_loan_app_with_decision(loan_amount: int, number_of_monthly_payment: int, loan_to_value: float,  first_name: str, last_name: str):
    loanRequest= LoanRequest(numberOfMonthlyPayments=number_of_monthly_payment, 
                             amount=loan_amount,
                             startDate=datetime.datetime.now(),
                             loanToValue=loan_to_value)
    
    borrower =  build_or_get_loan_client_repo().get_client_by_name(first_name=first_name, last_name=last_name)
    ds_request = Request(__DecisionID__= str(uuid.uuid4),borrower=borrower, loan=loanRequest)
    payload: str = ds_request.model_dump_json()
    return callRuleExecutionServer(payload)

    
methods = { "get_client_by_name": get_client_by_name, 
           "define_next_best_action_with_decision" : define_next_best_action_with_decision,
           "assess_loan_app_with_decision": assess_loan_app_with_decision}
arg_schemas = { "LoanRequest": LoanRequest}

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
    
class IbuLoanToolInstanceFactory(ToolInstanceFactoryInterface):
    
    def build_tool_instances(self, tool_entities: list[OwlToolEntity]) -> list[Any]:
        tool_list=[]
        for tool_entity in tool_entities:
            # TO DO rethink about this approach
            if tool_entity.tool_id == "tavily":
                tool_list.append(TavilySearchResults(max_results=2))
            elif "client" in tool_entity.tool_id:
                tool_list.append(define_tool( tool_entity.tool_description, tool_entity.tool_fct_name, tool_entity.tool_arg_schema_class)) # type: ignore
            elif  tool_entity.tool_id == "ibu_loan_assessment_action":
                tool_list.append(define_tool(tool_entity.tool_description, tool_entity.tool_fct_name, tool_entity.tool_arg_schema_class)) # type: ignore
            else:
                raise Exception("Not yet implemented")
        return tool_list
    