
import unittest

import requests

"""
Test the app at the api level using requests clients.
Run from folder above tests.

pytest -s tests/it/test_app_api.py

Goals: 
* address a general query to using the default prompt so it can validate reaching the selected LLM
"""

IBU_BASE_URL="http://localhost:8000/api/v1"

class TestAppApi(unittest.TestCase):

    def test_access_to_martin_client(self):
        """
        Verify the client is loaded by the agent executor
        """
        print("\n--> Validate client by id tool is called after decision from llm\n")
        data='{ "locale": "en",\
            "query": "who is the client with id 1?",\
            "chat_history": [],\
            "assistant_id":"ibu_assistant",  \
            "user_id" : "remote_test", \
            "thread_id" : "1" \
        }'
        rep = requests.post(IBU_BASE_URL + "/c/generic_chat", data=data, headers = {"Content-Type": "application/json"}).content.decode()
        print(f"\n@@@> {rep}")
        self.assertTrue(rep.find("David Martin") > 0 )

    def test_access_to_claim_information(self):
        """
        Verify the current claim of a customer is loaded
        """
        print("\n--> Validate getting claim is called\n")
        data='{ "locale": "en",\
            "query": "My name is Sonya Smith, I want to know the status of my current claim?",\
            "chat_history": [],\
            "assistant_id":"ibu_assistant",  \
            "user_id" : "remote_test", \
            "thread_id" : "2" \
        }'
        rep = requests.post(IBU_BASE_URL + "/c/generic_chat", data=data, headers = {"Content-Type": "application/json"}).content.decode()
        print(f"\n@@@> {rep}")
        #self.assertTrue(rep.find("David Martin") > 0 )
        
    def test_get_voucher_for_sonya(self):
        """
        Verify the voucher is proposed by the rules
        """
        print("\n--> Validate voucher is proposed\n")
        data='{ "locale": "en",\
            "query": "My name is Sonya Smith, I have problem with my claim 2 for my water damage, my carpet is expensive, I m surprise of the current coverage, very disappointing?",\
            "chat_history": [],\
            "assistant_id":"ibu_assistant",  \
            "user_id" : "remote_test", \
            "thread_id" : "2" \
        }'
        rep = requests.post(IBU_BASE_URL + "/c/generic_chat", data=data, headers = {"Content-Type": "application/json"}).content.decode()
        print(f"\n@@@> {rep}")
if __name__ == '__main__':
    unittest.main()