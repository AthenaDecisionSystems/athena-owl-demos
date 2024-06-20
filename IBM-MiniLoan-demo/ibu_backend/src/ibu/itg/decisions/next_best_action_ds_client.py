"""
Copyright 2024 Athena Decision Systems
@author Jerome Boyer
"""

import requests, logging, json
from athena.glossary.glossary_mgr import build_get_glossary, Glossary
from string import Template

LOGGER = logging.getLogger(__name__)

def _process_odm_response(odm_resp : str , glossary: Glossary, locale: str):
    pass

def callDecisionService(config, client_repo, client_id: int, locale: str = "en"):
    """
    Delegate the next best action to an external decision service
    """

    json_data = {}  # ADD payload prep here
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
    
