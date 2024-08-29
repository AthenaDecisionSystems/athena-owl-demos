import unittest
import sys, os
module_path = "./src"
sys.path.append(os.path.abspath(module_path))
os.environ["CONFIG_FILE"] = "./tests/ut/config/config.yaml"

from ibu.itg.ds.loanapp_borrower_repo import LoanApplicationClientRepositoryInterface
from ibu.itg.ds.loanapp_borrower_repo_mock import BorrowerRepositoryInMem

class TestClientRepository(unittest.TestCase):
    
    def test_access_one_client_by_id(self):
        repo: LoanApplicationClientRepositoryInterface = BorrowerRepositoryInMem()
        client = repo.get_client("robert dupont")
        assert client
        assert "robert" in client.name
    
    def test_access_one_client_by_name(self):
        repo: LoanApplicationClientRepositoryInterface = BorrowerRepositoryInMem()
        client = repo.get_client_by_name("Robert", "Smith")
        assert client
        assert "robert" in client.name
        
    def test_get_json_format(self):
        repo: LoanApplicationClientRepositoryInterface = BorrowerRepositoryInMem()
        client = repo.get_client_by_name_json("Robert", "Smith")
        assert client
        assert type(client) == str
        print(client)

if __name__ == '__main__':
    unittest.main()