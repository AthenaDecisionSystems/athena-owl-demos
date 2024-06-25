from athena.app_settings import AppSettings
from typing import Optional
from functools import lru_cache
import os, logging
from pydantic_yaml import parse_yaml_raw_as

class LoanAppSettings(AppSettings):
    app_borrower_repository: Optional[str] = ""
    app_loanapp_decision_service_url: Optional[str] = ""
    app_loan_repository: Optional[str] = ""
    
    
_config = None

# configuration is loaded only once and subsequent requests will use the cached configuration
@lru_cache
def get_config():
    global _config
    if _config is None:
        
        CONFIG_FILE= os.getenv("CONFIG_FILE")
        if CONFIG_FILE:
            print(f"reload config from file:{CONFIG_FILE}")
            with open(CONFIG_FILE, 'r') as file:
                _config = parse_yaml_raw_as(LoanAppSettings,file.read())
        else:
            _config = LoanAppSettings()
        if _config.logging_level == "INFO":
            _config.logging_level_int = logging.INFO
        if _config.logging_level == "DEBUG":
            _config.logging_level_int = logging.DEBUG
        else:
            _config.logging_level_int = logging.WARNING
    return _config