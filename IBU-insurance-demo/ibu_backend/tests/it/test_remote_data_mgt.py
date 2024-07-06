import unittest

import sys, os
os.environ["CONFIG_FILE"] = "./tests/it/config/config.yaml"
from dotenv import load_dotenv
load_dotenv("./.env")
sys.path.append('./src')

from ibu.itg.ds.insurance_client_repo_datamgr import InsuranceClientFromDataMgr
from ibu.itg.ds.insurance_claim_repo_datamgr import InsuranceClaimFromDataMgr
from ibu.itg.ds.insurance_claim_repo import InsuranceClaimRepositoryInterface
from ibu.itg.ds.insurance_client_repo import InsuranceClientRepositoryInterface
from ibu.itg.ds.ComplaintHandling_generated_model import *
from athena.app_settings import get_config
class TestRemoteDataManager(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):

        self.client_repo: InsuranceClientRepositoryInterface = InsuranceClientFromDataMgr()
        self.claim_repo: InsuranceClaimRepositoryInterface = InsuranceClaimFromDataMgr()

    def test_client_data_remote_access(self):
        """
        should retrieve client with id 1 and attributes need to be loaded
        """
      
        client = self.client_repo.get_client(1)
        self.assertEqual("Martin",client.lastName)

    def test_client_as_json(self):
        client = self.client_repo.get_client_json(2)
        self.assertEqual("Smith",client["lastName"])

    def test_claim_data_remote_access(self):
        claim: Claim = self.claim_repo.get_claim(2)
        assert claim.policy is not None
        print(claim)
    
    def test_claim_json_remote_access(self):
        claim_str=self.claim_repo.get_claim_json(2)
        print(f"\n ==> {claim_str}")
        self.assertEqual("IN_PROCESS_VERIFIED",claim_str["status"])

    def test_client_by_name_remote_access(self):
        client_str=self.client_repo.get_client_by_name_json("Martin")
        self.assertEqual("Martin",client_str["lastName"])



if __name__ == '__main__':
    unittest.main()