"""
Copyright 2024 Athena Decision Systems
@author Jerome Boyer
"""
import json,logging
from datetime import datetime
from ibu.app_settings import get_config, InsuranceAppSettings
from ibu.itg.ds.insurance_claim_repo import InsuranceClaimRepositoryInterface
from ibu.itg.ds.ComplaintHandling_generated_model import *


class InsuranceClaimFromFileSystem(InsuranceClaimRepositoryInterface):


    def __init__(self, config: Optional[InsuranceAppSettings]= None):
        if config:
            self.app_insurance_data_folder= config.app_insurance_data_folder
        else:    
            self.app_insurance_data_folder= get_config().app_insurance_data_folder     
        logging.info("Claims will be fetched from " + self.app_insurance_data_folder + "/claims")   
        self.CLAIMSDB = dict()
        self.initialize_claims_db()

    def add_claim(self, claim: Claim):
        self.CLAIMSDB[claim.id] = claim
    
    def initialize_claims_db(self):
        claim2 = Claim.parse_file(self.app_insurance_data_folder + "/claims/2.json")        
        self.add_claim(claim2)

        claim250303 = Claim.parse_file(self.app_insurance_data_folder + "/claims/250303.json")        
        self.add_claim(claim250303)
        
    def get_claim(self, id: int) -> Claim:
        logging.info(f"---> get claim with id: {id}")
        return self.CLAIMSDB.get(id, None)


    def get_claim_json(self, id: int) -> str:
        claim = self.get_claim(id)
        if claim == None:
            return f"No claim with id '{id}' found"
        return claim.model_dump_json()

    def get_all_claims_json(self) -> str:
        return json.dumps([claim.to_dict() for claim in self.CLAIMSDB.values()], indent=4)
    
    def get_all_claims(self) -> list[Claim]:
        return list(self.CLAIMSDB.values())