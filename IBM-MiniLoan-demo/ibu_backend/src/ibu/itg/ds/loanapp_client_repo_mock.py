"""
Copyright 2024 Athena Decision Systems
@author Jerome Boyer
"""
import json, logging
from ibu.itg.ds.loanapp_client_repo import LoanApplicationClientRepositoryInterface, Borrower

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
        self.add_client(Borrower(name="Bill", creditScore= 2, yearlyIncome=50000))


    def get_client_by_name(self, name: str) -> Borrower | None:
        for client in self.CLIENTDB.values():
            if client.name == name:
                return client
        return None


    def get_client_by_name_json(self, name: str) -> str:
        for client in self.CLIENTDB.values():
            if client.name == name:
                return client.model_dump_json()
        return f"No client found with name '{name}'"

    
    def get_all_clients_json(self) -> str:
        return json.dumps([client.model_dump() for client in self.CLIENTDB.values()], indent=4)


    def get_all_clients(self) -> list[Borrower]:
        return list(self.CLIENTDB.values())









