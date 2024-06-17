import unittest
import os, sys
from importlib import import_module

module_path = "./src"
sys.path.append(os.path.abspath(module_path))
from ibu.itg.ds import insurance_client_repo_mock

class TestClientRepository(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.repo = insurance_client_repo_mock.InsuranceClientInMem(None)

    def test_create_client_repo(self):
        self.repo = insurance_client_repo_mock.InsuranceClientInMem(None)
        client = self.repo.get_client_by_name("Martin")
        print(client)
        self.assertIsNotNone(client)

    def test_get_all(self):
        client = self.repo.get_all_clients_json()
        print(client)
        self.assertIsNotNone(client)


    def test_create_client_repo_dynamically(self):
        module_path= "ibu.itg.ds.insurance_client_repo_mock"
        class_name = "InsuranceClientInMem"
        mod = import_module(module_path)
        klass = getattr(mod, class_name)
        repo= klass(None)
        client=repo.get_client_by_name("Martin")
        print(client)
        self.assertIsNotNone(client)

    def test_create_claim_repo_dynamically(self):
        module_path= "ibu.itg.ds.insurance_claim_repo_mock"
        class_name = "InsuranceClaimInMem"
        mod = import_module(module_path)
        klass = getattr(mod, class_name)
        repo= klass(None)
        claim=repo.get_claim(1)
        print(claim)
        self.assertIsNotNone(claim)

if __name__ == '__main__':
    unittest.main()