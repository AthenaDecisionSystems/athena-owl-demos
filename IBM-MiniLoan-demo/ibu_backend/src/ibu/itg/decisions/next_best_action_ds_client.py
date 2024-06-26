"""
Copyright 2024 Athena Decision Systems
@author Jerome Boyer
"""

import requests
from ibu.app_settings import get_config

DS_URL: str = get_config().app_loanapp_decision_service_url # type: ignore

def callRuleExecutionServer(payload: str):
    response = requests.post(
        DS_URL, 
        payload,
        headers={"Content-Type": "application/json"}
    )
    return response


