"""
Copyright 2024 Athena Decision Systems
@author Jerome Boyer
"""
import logging
from typing import Optional, Any
from importlib import import_module

from athena.llm.tools.tool_mgr import DefaultToolInstanceFactory



LOGGER = logging.getLogger(__name__)


# ============================================= Function / Tool  Definitions ======================== 

def get_client_by_email_id(email: str) -> dict:
    """Get customer data given its unique email id"""

    country = "US"
    currency = "USD"
    if email.endswith(".uk"):
        country = "UK"
        currency = "GBP"
    elif email.endswith(".be"):
        country = "Belgium"
        currency = "EUR"
    elif email.endswith(".fr"):
        country = "France"
        currency = "EUR"
    elif email.endswith(".es"):
        country = "Spain"
        currency = "EUR"
    elif email.endswith(".it"):
        country = "Italy"
        currency = "EUR"

    return {
        "email": email,
        "date-of-birth": "1994-12-14",
        "income": 19500,
        "income_currency": currency,
        "country_of_residence": country
    }

        
class MyApplicationToolInstanceFactory(DefaultToolInstanceFactory):
    methods = {
        "get_client_by_email_id" : get_client_by_email_id
    }
