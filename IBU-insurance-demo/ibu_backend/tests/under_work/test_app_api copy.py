
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
        print("\n--> Validate Basic Query to LLM\n")
        data='{ "callWithVectorStore": false, "callWithDecisionService": false, "locale": "en",\
            "query": "who is the client with id 1?",\
            "type": "chat",\
            "modelParameters": { \
                "modelName": "gpt-3.5-turbo-0125",\
                "modelClass": "agent_openai",\
                "prompt_ref": "default_prompt",\
                "temperature": 0,\
                "top_k": 1,\
                "top_p": 1\
            },\
            "chat_history": ""\
            "assistant_id":"1"  \
            "user_id" : "remote_test" \
        }'
        rep = requests.post(IBU_BASE_URL + "/c/generic_chat", data=data, headers = {"Content-Type": "application/json"}).content.decode()
        print(f"\n@@@> {rep}")
  
        #self.assertTrue(resp.json()["message"].find("David Martin") > 0 )


"""_summary_
        
    def test_access_to_smith_client(self):
        """
        Verify the client is loaded by the agent using get by name
        """
        ctl = self.build_ConversationControl()
        ctl.query="what is the client with the name Smith ?"
        resp= self.client.post(get_config().api_route + "/c/generic_chat", json= ctl.model_dump())
        print(f"----> {resp.json()}")
        self.assertTrue(resp.json()["message"].find("Smith") > 0 )

    def test_not_existing_client(self):
        """
        Verify there is no client
        """
        ctl = self.build_ConversationControl()
        ctl.query="what is the client record for id=300 ?"
        resp=self.client.post(get_config().api_route + "/c/generic_chat", json= ctl.model_dump())
        print(f"----> {resp.json()}")
        self.assertTrue(resp.json()["message"].find("Not available") > 0  )

    def test_existing_claim(self):
        """
        Verify there is a claim using tools
        """
        ctl = self.build_ConversationControl()
        ctl.query="what is the claim record for id=1 ?"
        resp=self.client.post(get_config().api_route + "/c/generic_chat", json= ctl.model_dump())
        print(f"----> {resp.json()}")
        self.assertTrue(resp.json()["message"].find("IN_PROCESS_VERIFIED") > 0 or resp.json()["message"].find("in process") > 0)

    def test_what_is_the_best_Action_for_a_claim(self):
        msg="""
David Martin is not happy with the settlement of his claim with a claim_id 1. He thinks the amount reimbursed is far too low. 
He is threatening to leave to the competition.
"""
        ctl = self.build_ConversationControl()
        ctl.query=msg
        resp=self.client.post(get_config().api_route + "/c/generic_chat", json= ctl.model_dump())
        print(f"----> {resp.json()}")
        self.assertTrue(resp.json()["message"].find("Reassign") > 0)
        
"""


if __name__ == '__main__':
    unittest.main()