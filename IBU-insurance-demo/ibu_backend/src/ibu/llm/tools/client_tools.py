import logging
from athena.app_settings import get_config
from importlib import import_module
from langchain.tools import BaseTool, StructuredTool

LOGGER = logging.getLogger(__name__)

_insurance_client = None

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



def get_client_by_id(id: int) -> dict:
    """get insurance client information given its unique client identifier id"""
    return build_or_get_insurance_client_repo().get_client_json(id)

def get_client_by_name(name: str) -> dict:
    """get client information given his or her name"""
    return build_or_get_insurance_client_repo().get_client_by_name(name)

methods = {"get_client_by_id" : get_client_by_id, "get_client_by_name": get_client_by_name}

def define_tool(name: str, description: str, funct_name):
    return StructuredTool.from_function(
        func=methods[funct_name],
        name=name,
        description=description,
        #args_schema=,
        return_direct=False,
    )