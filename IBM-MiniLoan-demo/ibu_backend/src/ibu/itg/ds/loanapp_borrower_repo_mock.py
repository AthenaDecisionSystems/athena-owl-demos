"""
Copyright 2024 Athena Decision Systems
@author Jerome Boyer
"""
import json, logging
from ibu.itg.ds.loanapp_borrower_repo import LoanApplicationClientRepositoryInterface
from ibu.itg.ds.pydantic_generated_model import Borrower, Bankruptcy

class BorrowerRepositoryInMem(LoanApplicationClientRepositoryInterface):

    def __init__(self):
        self.BORROWERDB = dict()
        self.initialize_client_db()

    def add_client(self, client: Borrower):
        self.BORROWERDB[client.firstName] = client

    def get_client(self, id: int) -> Borrower:
        logging.info(f"---> In client mock get with id: {id}")
        return self.BORROWERDB.get(id, None)

    def initialize_client_db(self):
        self.add_client(Borrower(firstName = "Robert",
                            lastName = "Dupont",
                            birth = "2000-09-29",
                            SSN = None,
                            yearlyIncome = 50000,
                            zipCode = "ABC123",
                            creditScore = 180,
                            spouse = None,
                            latestBankruptcy = None
                            ))
        self.add_client(Borrower(firstName = "Joe",
                            lastName = "Hurt",
                            birth = "2000-03-01",
                            SSN = None,
                            yearlyIncome = 30000,
                            zipCode = "XYX999",
                            creditScore = 700,
                            spouse = None,
                            latestBankruptcy = None
                            ))
        self.add_client(Borrower(firstName = "Marie",
                            lastName = "Durand",
                            birth = "1990-03-01",
                            SSN = None,
                            yearlyIncome = 80000,
                            zipCode = "XYX999",
                            creditScore = 500,
                            spouse = None,
                            latestBankruptcy = None
                            ))
        self.add_client(Borrower(firstName = "Jean",
                            lastName = "Martin",
                            birth = "1980-12-17",
                            SSN = None,
                            yearlyIncome = 100000,
                            zipCode = "PQR123",
                            creditScore = 500,
                            spouse = None,
                            latestBankruptcy = None
                            ))
        self.add_client(Borrower(firstName = "Sophie",
                            lastName = "Lefevre",
                            birth = "1999-04-27",
                            SSN = None,
                            yearlyIncome = 40000,
                            zipCode = "MNP376",
                            creditScore = 500,
                            spouse = None,
                            latestBankruptcy = None
                            ))
        self.add_client(Borrower(firstName = "Pierre",
                            lastName = "Moreau",
                            birth = "1970-07-04",
                            SSN = None,
                            yearlyIncome = 120000,
                            zipCode = "CVZ517",
                            creditScore = 500,
                            spouse = None,
                            latestBankruptcy = None
                            ))
        bk=Bankruptcy(date="2018-11-20", chapter="11", reason="out of business")
        rsmith = Borrower(firstName = "Robert",
                            lastName = "Smith",
                            birth = "1985-10-04",
                            SSN = None,
                            yearlyIncome = 140000,
                            zipCode = "VCT291",
                            creditScore = 150,
                            latestBankruptcy = bk
                            )
        self.add_client(rsmith)


    def get_client_by_name(self, first_name: str, last_name: str) -> Borrower | None:
        for client in self.BORROWERDB.values():
            if client.firstName == first_name and client.lastName == last_name:
                return client
        return None


    def get_client_by_name_json(self, first_name: str, last_name: str) -> str:
        client = self.get_client_by_name(first_name, last_name)
        if client:
            return client.model_dump_json()
        return f"No client found with name '{first_name} - {last_name}'"

    
    def get_all_clients_json(self) -> str:
        return json.dumps([client.model_dump() for client in self.BORROWERDB.values()], indent=4)


    def get_all_clients(self) -> list[Borrower]:
        return list(self.BORROWERDB.values())









