"""
Copyright 2024 Athena Decision Systems
@author Jerome Boyer
"""
import json, logging
from .insurance_client_repo import InsuranceClientRepositoryInterface
from .ComplaintHandling_generated_model import *

class InsuranceClientInMem(InsuranceClientRepositoryInterface):

    def __init__(self,config):
        self.CLIENTDB = dict()
        self.initialize_client_db()

    def add_client(self, client: Client):
        self.CLIENTDB[client.id] = client

    def get_client(self, id: int) -> Client:
        logging.info(f"---> In client mock get with id: {id}")
        return self.CLIENTDB.get(id, None)

    def initialize_client_db(self):
        self.add_client(Client(id=1,firstName = "Robert",
                            lastName = "Dupont",
                            paymentScore=3,
                            claimsScore=1,
                            vip=False,
                            preferredChannel= PreferredChannel.mail
                            ))
        self.add_client(Client(id=2,
                            firstName = "Marie",
                            lastName = "Durand",
                            paymentScore=3,
                            claimsScore=1,
                            vip=False,
                            preferredChannel= PreferredChannel.mail
                            ))
        self.add_client(Client(id=3,
                            firstName = "Jean",
                            lastName = "Martin",
                            paymentScore=2,
                            claimsScore=3,
                            vip=False,
                            preferredChannel= PreferredChannel.SMS
                            ))
        self.add_client(Client(id=4,
                            firstName = "Sophie",
                            lastName = "Lefevre",
                            paymentScore=2,
                            claimsScore=1,
                            vip=False,
                            preferredChannel= PreferredChannel.SMS
                            ))
        self.add_client(Client(id=5,
                            firstName = "Pierre",
                            lastName = "Moreau",
                            paymentScore=3,
                            claimsScore=3,
                            vip=False,
                            preferredChannel= PreferredChannel.SMS
                            ))
        self.add_client(Client(id=6,
                            firstName = "Isabelle",
                            lastName = "Girard",
                            paymentScore=3,
                            claimsScore=2,
                            vip=True,
                            preferredChannel= PreferredChannel.phone
                            ))
        self.add_client(Client(id=7,
                            firstName = "Roberto",
                            lastName = "de la Fuente",
                            paymentScore=3,
                            claimsScore=3,
                            vip=False,
                            preferredChannel= PreferredChannel.mail
                            ))
        self.add_client(Client(id=8,
                            firstName = "Robert",
                            lastName = "Smith",
                            paymentScore=3,
                            claimsScore=3,
                            vip=False,
                            preferredChannel= PreferredChannel.mail
                            ))


    def get_client_by_name(self, lastName: str) -> Client:
        for client in self.CLIENTDB.values():
            if client.lastName == lastName:
                return client
        return None


    def get_client_by_name_json(self, lastName: str) -> Client:
        for client in self.CLIENTDB.values():
            if client.lastName == lastName:
                return client.to_json()
        return f"No client found with name '{lastName}'"

    def get_client_json(self, id: int) -> str:
        client = self.get_client(id)
        if client == None:
            return f"No client with id '{id}' found"
        return client.to_json()

    def get_all_clients_json(self) -> str:
        return json.dumps([client.to_dict() for client in self.CLIENTDB.values()], indent=4)


    def get_all_clients(self) -> list[Client]:
        return list(self.CLIENTDB.values())









