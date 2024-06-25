import unittest
import sys, os
os.environ["CONFIG_FILE"] = "./tests/ut/config/config.yaml"
module_path = "./src"
sys.path.append(os.path.abspath(module_path))

from ibu.app_settings import get_config
from ibu.itg.ds.pydantic_generated_model import Request, LoanRequest, Borrower
from ibu.itg.decisions.next_best_action_ds_client import callRuleExecutionServer
from ibu.itg.ds.loanapp_borrower_repo_mock import BorrowerRepositoryInMem



class TestLoanDecisionServiceBackend(unittest.TestCase):
    
    def test_good_borrower(self):    
        print("\n\n---- good borrower")
        request = Request(loan=LoanRequest(
            numberOfMonthlyPayments= 12,
            startDate = "2006-08-19T19:27:14.000+0200",
            amount = 100000,
            
            loanToValue= 0.7
                        ),
            borrower=Borrower(
                firstName = "Joe",
                lastName = "Hurt",
                birth = "2000-09-29",
                SSN = None,
                yearlyIncome = 50000,
                zipCode = "ABC123",
                creditScore = 3,
                spouse = None,
                latestBankruptcy = None)
        )
        payload: str = request.model_dump_json()
        resp = callRuleExecutionServer(payload)
        response_json = resp.json()
        print(response_json)
        
    def test_using_repo_to_get_low_credit_score_user_borrower(self):
        print("\n\n---- test_using_repo_to_get_bankrupted_borrower")
        repo =BorrowerRepositoryInMem()
        rsmith = repo.get_client_by_name(first_name = "Robert", last_name = "Smith")
        request = Request(loan=LoanRequest(
            numberOfMonthlyPayments= 12,
            startDate = "2006-08-19T19:27:14.000+0200",
            amount = 1000000,
            loanToValue= 0.7),
            borrower=rsmith)
        payload: str = request.model_dump_json()
        resp = callRuleExecutionServer(payload)
        response_json = resp.json()
        print(response_json)