"""
Copyright 2024 Athena Decision Systems
@author Jerome Boyer
"""
import json, logging
from ibu.itg.ds.insurance_client_repo import InsuranceClientRepositoryInterface
from ibu.itg.ds.ComplaintHandling_generated_model import *

class InsuranceClientInMem(InsuranceClientRepositoryInterface):

    def __init__(self):
        self.CLIENTDB = dict()
        self.initialize_client_db()

    def add_client(self, client: Client):
        self.CLIENTDB[client.id] = client

    def get_client(self, id: int) -> Client:
        logging.info(f"---> In client mock get with id: {id}")
        return self.CLIENTDB.get(id, None)

    def initialize_client_db(self):
        self.add_client(Client(id=1,
                            firstName = "David",
                            lastName = "Martin",
                            dateOfBirth = "1967-02-22T00:00:00.000+00:00",
                            firstContractDate = "2005-10-31T00:00:00.000+00:00",
                            cltvPercentile = 56,
                            propensityToUpgradePolicy= 0.55,

                            preferredChannel= PreferredChannel.mail
                            ))
        self.add_client(Client(id=2,
                            firstName = "Sonya",
                            lastName = "Smith",
                            dateOfBirth = "1999-03-12T00:00:00.000+00:00",
                            firstContractDate = "2023-11-12T00:00:00.000+00:00",
                            cltvPercentile = 62,
                            propensityToUpgradePolicy= 0.61,
                            preferredChannel= PreferredChannel.phone
                            ))
        self.add_client(Client(id=3,
                            firstName = "Zoe",
                            lastName = "Durand",
                            dateOfBirth = "2001-10-31T00:00:00.000+00:00",
                            firstContractDate = "2024-01-15T00:00:00.000+00:00",
                            cltvPercentile = 44,
                            propensityToUpgradePolicy= 0.19,
                            preferredChannel= PreferredChannel.email
                            ))
        self.add_client(Client(id=4,
                            firstName = "Robert",
                            lastName = "Smith",
                            dateOfBirth = "1660-08-26T00:00:00.000+00:00",
                            firstContractDate = "2014-01-15T00:00:00.000+00:00",
                            cltvPercentile = 44,
                            propensityToUpgradePolicy= 0.19,
                            preferredChannel= PreferredChannel.SMS
                            ))


    def get_client_by_name(self, firstname: str, lastname: str) -> Client:
        for client in self.CLIENTDB.values():
            if client.lastName == lastname and client.firstname == firstname:
                return client
        return None


    def get_client_by_name_json(self, firstname: str, lastname: str) -> str:
        for client in self.CLIENTDB.values():
            if client.lastName == lastname and client.firstname == firstname:
                return client.model_dump_json()
        return f"No client found with name '{lastname}'"

    def get_client_json(self, id: int) -> str:
        client = self.get_client(id)
        if client == None:
            return f"No client with id '{id}' found"
        return client.model_dump_json()

    def get_all_clients_json(self) -> str:
        return json.dumps([client.model_dump() for client in self.CLIENTDB.values()], indent=4)


    def get_all_clients(self) -> list[Client]:
        return list(self.CLIENTDB.values())









