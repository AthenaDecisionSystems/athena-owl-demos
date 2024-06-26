
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
        data='{ "callWithVectorStore": false, "callWithDecisionService": false, "locale": "en",\
            "query": "who is the client with id 1?",\
            "type": "chat",\
            "chat_history": [],\
            "assistant_id":"ibu_assistant",  \
            "user_id" : "remote_test" \
        }'
        rep = requests.post(IBU_BASE_URL + "/c/generic_chat", data=data, headers = {"Content-Type": "application/json"}).content.decode()
        print(f"\n@@@> {rep}")
  
        #self.assertTrue(resp.json()["message"].find("David Martin") > 0 )

if __name__ == '__main__':
    unittest.main()