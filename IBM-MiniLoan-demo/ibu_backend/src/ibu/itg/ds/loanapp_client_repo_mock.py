"""
Copyright 2024 Athena Decision Systems
@author Jerome Boyer
"""
import json, logging
from ibu.itg.ds.loanapp_client_repo import LoanApplicationClientRepositoryInterface
from .pydantic_generated_model import *

class LoanAppRepositoryInMem(LoanApplicationClientRepositoryInterface):

    def __init__(self, config):
        self.CLIENTDB = dict()
        self.initialize_client_db()

    def add_client(self, client: Borrower):
        self.CLIENTDB[client.name] = client

    def get_client(self, id: int) -> Borrower:
        logging.info(f"---> In client mock get with id: {id}")
        return self.CLIENTDB.get(id, None)

    def initialize_client_db(self):
        self.add_client(Borrower(firstName = "Robert",
                            lastName = "Dupont",
                            birth = "2000-09-29",
                            SSN = None,
                            yearlyIncome = 50000,
                            zipCode = "ABC123",
                            creditScore = 5,
                            spouse = None,
                            latestBankruptcy = None
                            ))
        self.add_client(Borrower(firstName = "Joe",
                            lastName = "Hurt",
                            birth = "2000-03-01",
                            SSN = None,
                            yearlyIncome = 30000,
                            zipCode = "XYX999",
                            creditScore = 3,
                            spouse = None,
                            latestBankruptcy = None
                            ))
        self.add_client(Borrower(firstName = "Marie",
                            lastName = "Durand",
                            birth = "1990-03-01",
                            SSN = None,
                            yearlyIncome = 80000,
                            zipCode = "XYX999",
                            creditScore = 6,
                            spouse = None,
                            latestBankruptcy = None
                            ))
        self.add_client(Borrower(firstName = "Jean",
                            lastName = "Martin",
                            birth = "1980-12-17",
                            SSN = None,
                            yearlyIncome = 100000,
                            zipCode = "PQR123",
                            creditScore = 8,
                            spouse = None,
                            latestBankruptcy = None
                            ))
        self.add_client(Borrower(firstName = "Sophie",
                            lastName = "Lefevre",
                            birth = "1999-04-27",
                            SSN = None,
                            yearlyIncome = 40000,
                            zipCode = "MNP376",
                            creditScore = 4,
                            spouse = None,
                            latestBankruptcy = None
                            ))
        self.add_client(Borrower(firstName = "Pierre",
                            lastName = "Moreau",
                            birth = "1970-07-04",
                            SSN = None,
                            yearlyIncome = 120000,
                            zipCode = "CVZ517",
                            creditScore = 5,
                            spouse = None,
                            latestBankruptcy = None
                            ))
        self.add_client(Borrower(firstName = "Robert",
                            lastName = "Smith",
                            birth = "1985-10-04",
                            SSN = None,
                            yearlyIncome = 140000,
                            zipCode = "VCT291",
                            creditScore = 9,
                            spouse = None,
                            latestBankruptcy = None
                            ))


    def get_client_by_name(self, first_name: str, last_name: str) -> Borrower | None:
        for client in self.CLIENTDB.values():
            if client.firstName == first_name and client.lastName == last_name:
                return client
        return None


    def get_client_by_name_json(self, first_name: str, last_name: str) -> str:
        for client in self.CLIENTDB.values():
            if client.firstName == first_name and client.lastName == last_name:
                return client.model_dump_json()
        return f"No client found with name '{first_name}'"

    
    def get_all_clients_json(self) -> str:
        return json.dumps([client.model_dump() for client in self.CLIENTDB.values()], indent=4)


    def get_all_clients(self) -> list[Borrower]:
        return list(self.CLIENTDB.values())









