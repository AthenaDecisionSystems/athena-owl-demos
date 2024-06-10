"""
Copyright 2024 Athena Decision Systems
@author Jerome Boyer
"""
import json, logging
import requests
from fastapi.encoders import jsonable_encoder
from .insurance_claim_repo import InsuranceClaimRepositoryInterface
from .ComplaintHandling_generated_model import *
LOGGER = logging.getLogger(__name__)


class InsuranceClaimFromDataMgr(InsuranceClaimRepositoryInterface):

    def __init__(self,config):
        self.data_mgr_url= config.app_insurance_backend_url
        
    def get_all_claims(self) -> list[Claim]:
        resp = []
        try:
            resp=requests.get(self.data_mgr_url + "/claims/")
            LOGGER.info(resp.text)
        except:
            LOGGER.error("Issue contacting the claim repository backend")
        return resp
    
    def get_claim(self, id: int) -> Claim:
        claim = None
        try:
            resp=requests.get(self.data_mgr_url + "/claims/" + str(id))
            LOGGER.debug(resp.text)
            ## TO DO align claim structure 
            claim = Claim(**json.loads(resp.text))
            #claim=resp.text
        except:
            LOGGER.error("Issue contacting the claim repository backend")
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
    










