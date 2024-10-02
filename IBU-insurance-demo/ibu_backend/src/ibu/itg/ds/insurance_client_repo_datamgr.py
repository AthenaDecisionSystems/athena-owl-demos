"""
Copyright 2024 Athena Decision Systems
@author Jerome Boyer
"""
import json, logging
import requests
from typing import Optional
from fastapi.encoders import jsonable_encoder
from ibu.app_settings import get_config, InsuranceAppSettings
from ibu.itg.ds.insurance_client_repo import InsuranceClientRepositoryInterface
from ibu.itg.ds.ComplaintHandling_generated_model import *
LOGGER = logging.getLogger(__name__)


class InsuranceClientFromDataMgr(InsuranceClientRepositoryInterface):

    def __init__(self, config: Optional[InsuranceAppSettings]):
        if config:
            self.data_mgr_url= config.app_insurance_backend_url
        else:    
            self.data_mgr_url= get_config().app_insurance_backend_url
        

    def get_client(self, id: int) -> Client:
        client = None
        try:
            resp=requests.get(self.data_mgr_url + "/clients/" + str(id))
            client = Client(**json.loads(resp.text))
            #client= resp.text
        except:
            LOGGER.error("Issue contacting the client repository backend")
        return client


    def get_client_by_name(self, firstname: str, lastname: str) -> Client:
        client = None
        try:
            resp=requests.get(self.data_mgr_url + "/clients/search/" + firstname + "/" + lastname)
            client = Client(**json.loads(resp.text))
        except:
            LOGGER.error("Issue contacting the client repository backend")
        return client

    def get_client_by_name_json(self, firstname: str, lastname: str) -> str:
        client = self.get_client_by_name(firstname, lastname)
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









