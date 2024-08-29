"""
Test decision service client with repository to validate data model serialization
"""

import unittest
import sys, os
module_path = "./src"
sys.path.append(os.path.abspath(module_path))
os.environ["CONFIG_FILE"] = "./tests/ut/config/config.yaml"
from ibu.itg.ds.loanapp_borrower_repo import LoanApplicationClientRepositoryInterface
from ibu.itg.ds.loanapp_borrower_repo_mock import BorrowerRepositoryInMem
from ibu.itg.decisions.next_best_action_ds_client import callRuleExecutionServer
from ibu.llm.tools.client_tools import assess_loan_app_with_decision
from ibu.itg.ds.pydantic_generated_model import Request, Borrower, Loan, Response

class TestMiniLoanIntegration(unittest.TestCase):
    
    
    def test_too_high_loan(self):
        """Test at the decision service client level"""
        repo: LoanApplicationClientRepositoryInterface = BorrowerRepositoryInMem()
        borrower: Borrower = repo.get_client_by_name("Robert", "Smith")
        loanRequest= Loan(duration=120, 
                      yearlyRepayment=100000,
                      yearlyInterestRate=4,
                      amount=3000000)
        ds_request = Request(borrower=borrower, loan=loanRequest) # type: ignore
        payload: str = ds_request.model_dump_json()
        print(payload)
        rep = callRuleExecutionServer(payload)
        assert rep.text
        print(f"\n\n-> {rep.text}")
        odm_rep : Response = Response.model_validate_json(rep.text)
        print(f"\n\n-> {odm_rep.loan.messages}")
        assert "The loan cannot exceed 1,000,000" in odm_rep.loan.messages[0]
        assert not odm_rep.loan.approved
        
    def test_high_deb_to_income(self):
        """Test at the decision service client level"""
        print("\n\n--- test_high_deb_to_income ---\n")
        repo: LoanApplicationClientRepositoryInterface = BorrowerRepositoryInMem()
        borrower: Borrower = repo.get_client("sophie lefevre")
        loanRequest= Loan(duration=120, 
                      yearlyRepayment=100000,
                      yearlyInterestRate=4,
                      amount=300000)
        ds_request = Request(borrower=borrower, loan=loanRequest) # type: ignore
        payload: str = ds_request.model_dump_json()
        print(payload)
        rep = callRuleExecutionServer(payload)
        assert rep.text
        print(f"\n\n-> {rep.text}")
        odm_rep : Response = Response.model_validate_json(rep.text)
        print(f"\n\n-> {odm_rep.loan.messages}")
        assert not odm_rep.loan.approved
        
    def test_low_credit_score(self):
        """Test at the function call level"""
        print("\n\n--- test_low_credit_score ---\n")
        rep = assess_loan_app_with_decision(loan_amount=300000, duration=120,   first_name="robert", last_name= "smith", yearlyRepayment=100000)

        print(f"\n\n-> {rep}")
        odm_rep : Response = Response.model_validate_json(rep)
        print(f"\n\n-> {odm_rep.loan.messages}")
        assert not odm_rep.loan.approved
        
    def test_approved(self):
        """Test at the decision service client level"""
        print("\n\n--- test_approved ---\n")
        repo: LoanApplicationClientRepositoryInterface = BorrowerRepositoryInMem()
        borrower: Borrower = repo.get_client("jean martin")
        loanRequest= Loan(duration=120, 
                      yearlyRepayment=10000,
                      yearlyInterestRate=4,
                      amount=300000)
        ds_request = Request(borrower=borrower, loan=loanRequest) # type: ignore
        payload: str = ds_request.model_dump_json()
        print(payload)
        rep = callRuleExecutionServer(payload)
        assert rep.text
        print(f"\n\n-> {rep.text}")
        odm_rep : Response = Response.model_validate_json(rep.text)
        print(f"\n\n-> {odm_rep.loan.messages}")
        assert odm_rep.loan.approved
        
    def test_small_loan_approved(self):
        """Test at the function call level"""
        print("\n\n--- test_small_loan_approved ---\n")
       
        rep = assess_loan_app_with_decision(loan_amount=20000, duration=60,   first_name="robert", last_name= "dupont", yearlyRepayment=4000)
        print(f"\n\n-> {rep}")
        odm_rep : Response = Response.model_validate_json(rep)
        print(f"\n\n-> {odm_rep.loan.messages}")
        assert odm_rep.loan.approved

if __name__ == '__main__':
    unittest.main()