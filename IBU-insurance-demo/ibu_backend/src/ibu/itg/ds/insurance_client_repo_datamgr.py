"""
Copyright 2024 Athena Decision Systems
@author Jerome Boyer
"""
import json, logging
import requests
from fastapi.encoders import jsonable_encoder
from .insurance_client_repo import InsuranceClientRepositoryInterface
from .ComplaintHandling_generated_model import *
LOGGER = logging.getLogger(__name__)


class InsuranceClientFromDataMgr(InsuranceClientRepositoryInterface):

    def __init__(self,config):
        self.data_mgr_url= config.app_insurance_backend_url
        

    def get_client(self, id: int) -> Client:
        client = None
        try:
            resp=requests.get(self.data_mgr_url + "/clients/" + str(id))
            client = Client(**json.loads(resp.text))
            #client= resp.text
        except:
            LOGGER.error("Issue contacting the client repository backend")
        return client


    def get_client_by_name(self, name: str) -> Client:
        client = None
        try:
            resp=requests.get(self.data_mgr_url + "/clients/search/" + name)
            client = Client(**json.loads(resp.text))
        except:
            LOGGER.error("Issue contacting the client repository backend")
        return client

    def get_client_by_name_json(self, name: str) -> str:
        client = self.get_client_by_name(name)
        if client != None:
            return  jsonable_encoder(client)
        return ""


    def get_client_json(self, id: int) -> str:
        client = self.get_client(id)
        if client != None:
            return  jsonable_encoder(client)
        return ""

    def get_all_clients_json(self) -> str:
        clients = self.get_all_clients()
        if clients != None:
            return  jsonable_encoder(clients)
        return ""


    def get_all_clients(self) -> list[Client]:
        resp = []
        try:
            resp=requests.get(self.data_mgr_url + "/clients/")
            LOGGER.info(resp)
        except:
            LOGGER.error("Issue contacting the client repository backend")
        return resp









