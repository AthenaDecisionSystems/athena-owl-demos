"""
Copyright 2024 Athena Decision Systems
@author Jerome Boyer
"""
from pydantic import BaseModel
from typing import List
import json

class Borrower(BaseModel):
    name: str = ""
    creditScore: int = 0
    yearlyIncome: int = 60000
 
class Loan(BaseModel):
    amount: int = 0
    duration: int =0
    yearlyInterestRate: float = 0
    yearlyRepayment: int = 0
    approved: bool = False
    messages: List[str] = []

class LoanApplicationClientRepositoryInterface:

    def add_client(self,client: Borrower):
        pass

    def get_client_by_name(self,name: str) -> Borrower | None:
        return None
    
    def get_client_by_name_json(self, name: str) -> str | None:
        return None
    
    def get_all_clients_json(self) -> str | None:
        return None
    
    def get_all_clients(self) -> list[Borrower] | None:
        return None