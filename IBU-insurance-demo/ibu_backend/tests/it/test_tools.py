import unittest

import sys,os
from dotenv import load_dotenv
load_dotenv()

os.environ["CONFIG_FILE"] = "./tests/it/config/config.yaml"
module_path = "./src"
sys.path.append(os.path.abspath(module_path))
from ibu.llm.tools.client_tools import get_client_by_name, get_claim_by_id, get_client_by_id, get_claim_status_by_user_name
from ibu.itg.ds.ComplaintHandling_generated_model import Status

class TestTools(unittest.TestCase):
    
    def get_client_by_name(self):
        client = get_client_by_name("Sonya", "Smith")
        assert client
        assert "Sonya" in client.firstName 
        print(client)

    def test_client(self):
        client = get_client_by_id("2")
        assert client
        assert "Sonya" in client["firstName"] 
        print(client)

    def test_claim(self):
        claim = get_claim_by_id("2")
        assert claim
        print(claim)
        assert "IN_PROCESS_VERIFIED" in claim["status"]

    def test_get_claim_status_by_user_name(self):
        claimStatus = get_claim_status_by_user_name("Sonya", "Smith")
        assert claimStatus
        print(claimStatus)
        assert Status.IN_PROCESS_VERIFIED == claimStatus


if __name__ == '__main__':
    unittest.main()