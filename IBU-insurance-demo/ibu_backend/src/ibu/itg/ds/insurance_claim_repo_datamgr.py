"""
Copyright 2024 Athena Decision Systems
@author Jerome Boyer
"""
import json, logging
import requests
from typing import Optional
from fastapi.encoders import jsonable_encoder
from ibu.app_settings import get_config, InsuranceAppSettings
from ibu.itg.ds.insurance_claim_repo import InsuranceClaimRepositoryInterface
from ibu.itg.ds.ComplaintHandling_generated_model import *
LOGGER = logging.getLogger(__name__)


class InsuranceClaimFromDataMgr(InsuranceClaimRepositoryInterface):

    def __init__(self, config: Optional[InsuranceAppSettings]= None):
        if config:
            self.data_mgr_url= config.app_insurance_backend_url
        else:    
            self.data_mgr_url= get_config().app_insurance_backend_url
        
    def get_all_claims(self) -> list[Claim]:
        resp = []
        try:
            resp=requests.get(self.data_mgr_url + "/claims/")
            LOGGER.info(resp.json())
        except Exception as e:
            LOGGER.error(f"Issue contacting the claim repository backend: {e}")
        return resp.json()
    
    def get_claim(self, id: int) -> Claim:
        claim = None
        try:
            resp=requests.get(self.data_mgr_url + "/claims/" + str(id))
            LOGGER.debug(resp.text)
            ## TO DO align claim structure 
            claim = Claim(**json.loads(resp.text))
            #claim=resp.text
        except Exception as e:
            LOGGER.error(f"Issue contacting the claim repository backend: {e}")
        return claim
    
    def get_claim_json(self, id: int) -> str:
        claim = self.get_claim(id)
        if claim != None:
            return  jsonable_encoder(claim)
        return None

    def get_all_claims_json(self) -> str:
        claims = self.get_all_claims()
        if claims != None:
            return  jsonable_encoder(claims)
        return None
    










