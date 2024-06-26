import unittest
import sys, os
os.environ["CONFIG_FILE"] = "./tests/ut/config/config.yaml"
module_path = "./src"
sys.path.append(os.path.abspath(module_path))

from ibu.app_settings import get_config
from ibu.itg.ds.pydantic_generated_model import Request, Loan, Borrower
from ibu.itg.decisions.next_best_action_ds_client import callRuleExecutionServer
from ibu.itg.ds.loanapp_borrower_repo_mock import BorrowerRepositoryInMem



class TestLoanDecisionServiceBackend(unittest.TestCase):
    
    def test_good_borrower(self):    
        print("\n\n---- good borrower\n\n")
        request = Request(loan=Loan(
            duration= 36,
            yearlyInterestRate= 5,
            yearlyRepayment=3000,
            amount = 90000),
            borrower=Borrower(
                name = "Joe Hurt",
                yearlyIncome = 90000,
                creditScore = 500)
        )
        payload: str = request.model_dump_json()
        print(f"request to rule execution server: {request}\n")
        resp = callRuleExecutionServer(payload)
        response_json = resp.json()
        print(f"--> response from rule execution server: {response_json}")
        
    def test_using_repo_to_get_low_credit_score_user_borrower(self):
        print("\n\n---- test_using_repo_to_get_bankrupted_borrower")
        repo =BorrowerRepositoryInMem()
        rsmith = repo.get_client_by_name(first_name = "Robert", last_name = "Smith")
        request = Request(loan=Loan(
            duration= 60,
            yearlyRepayment=3000,
            yearlyInterestRate= 5,
            amount = 100000),
            borrower=rsmith)
        payload: str = request.model_dump_json()
        print(f"request to rule execution server: {request}\n")
        resp = callRuleExecutionServer(payload)
        response_json = resp.json()
        print(f"--> response from rule execution server: {response_json}")