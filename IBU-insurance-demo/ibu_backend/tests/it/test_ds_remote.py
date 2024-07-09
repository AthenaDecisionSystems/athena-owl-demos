
import unittest

import sys
sys.path.append('./src')
from ibu.itg.decisions.next_best_action_ds_client import callDecisionService
from ibu.itg.ds.ComplaintHandling_generated_model import Motive 
from ibu.itg.ds.insurance_claim_repo_datamgr import InsuranceClaimFromDataMgr
from ibu.app_settings import AppSettings


class TestDecisionServiceRemote(unittest.TestCase):

    def test_best_action_for_claim_1(self):
        motive = Motive.UnsatisfiedWithReimbursedAmount
        config = AppSettings()
        config.owl_best_action_ds_url= "http://localhost:9060/DecisionService/rest/v1/ComplaintHandling/1.0/nextBestAction"
        config.owl_glossary_path=  "./config/glossary.json"
        config.app_insurance_backend_url="http://localhost:8080/repository"
        repo=InsuranceClaimFromDataMgr(config)
        rep = callDecisionService(config, repo,1,motive,True,"en")
        print(rep)



if __name__ == '__main__':
    unittest.main()