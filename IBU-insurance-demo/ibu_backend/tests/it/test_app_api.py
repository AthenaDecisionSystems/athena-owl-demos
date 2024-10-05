
import unittest

import requests
import json
import sys
sys.path.append('./src')

from athena.routers.dto_models import ConversationControl
"""
Test the app at the api level using requests clients.
Run from folder above tests.

pytest -s tests/it/test_app_api.py

Goals: 
* address a general query to using the default prompt so it can validate reaching the selected LLM
"""

IBU_BASE_URL="http://localhost:8002/api/v1"

class TestAppApi(unittest.TestCase):

    def define_data_as_string(self,query: str, thread_id: str) -> str:
        cc = ConversationControl()
        cc.agent_id="ibu_agent"
        cc.user_id="remote_test"
        cc.thread_id=thread_id
        cc.chat_history=[]
        cc.query=query
        return cc.model_dump_json()

    def get_response_content(self, rep) -> str:
        print(f"\n@@@> {rep}")
        rep_dict= json.loads(rep)
        return rep_dict["messages"][0]["content"]
    
    def test_1_access_to_martin_client(self):
        """
        Verify the client is loaded by the agent executor
        """
        print("\n--> #1 Validate client by id tool is called after decision from llm\n")
        data=self.define_data_as_string("who is the client with id 1?","1")
        rep = requests.post(IBU_BASE_URL + "/c/generic_chat", data=data, headers = {"Content-Type": "application/json"}, timeout = 10).content.decode()
        content= self.get_response_content(rep)
        self.assertTrue(content.find("David Martin") > 0 )

    def test_2_access_to_claim_information(self):
        """
        Verify the current claim of a customer is loaded
        """
        print("\n--> #2 Validate getting claim is called\n")
        data=self.define_data_as_string("My name is Sonya Smith, I want to know the status of my current claim?","2")
        rep = requests.post(IBU_BASE_URL + "/c/generic_chat", data=data, headers = {"Content-Type": "application/json"}).content.decode()
        content= self.get_response_content(rep).lower()
        self.assertTrue(content.find("process") > 0 )
        self.assertTrue(content.find("verified") > 0 )
        
    def test_3_get_voucher_for_sonya(self):
        """
        Verify the voucher is proposed by the rules
        """
        print("\n--> Validate voucher is proposed for Sonya Smith\n")
        data=self.define_data_as_string("Hi IBU, I am on the phone with one of my very important customer. Her name is Sonya Smith. She has a problem with her claim 2 for their water damage. She told me that the carpet is expensive. She is surprised of the current coverage. Sonya finds this very disappointing. What would be the next best action?","3")
        rep = requests.post(IBU_BASE_URL + "/c/generic_chat", data=data, headers = {"Content-Type": "application/json"}).content.decode()
        content= self.get_response_content(rep).lower()
        print(f"\n@@@> {content}")
        rep = requests.get(IBU_BASE_URL + "/c/conversation/trace/3")
        print(f"\n@@@> {rep}")


if __name__ == '__main__':
    unittest.main()