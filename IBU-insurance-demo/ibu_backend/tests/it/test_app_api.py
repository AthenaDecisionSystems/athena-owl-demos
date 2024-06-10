
import unittest
import sys,os
os.environ["CONFIG_FILE"] = "./tests/it/config/config.yaml"
from dotenv import load_dotenv
load_dotenv("./.env")
sys.path.append('./src')
from ibu.main import app
from athena.app_settings import  get_config
from athena.routers.dto_models import ConversationControl
from athena.routers.prompt import PromptRequest
from fastapi.testclient import TestClient

"""
Test the app at the api level using FastAPI test client, and the configuration for integration tests.
Run from folder above tests.

pytest -s tests/it/test_app_api.py

Goals: 
* validate health and version paths
* address a general query to using the default prompt so it can validate reaching the selected LLM
"""
class TestAppApi(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):
        self.client = TestClient(app)
        print("init test done")
       

    def build_ConversationControl(self):
        ctl = ConversationControl()
        ctl.callWithVectorStore = False
        ctl.callWithDecisionService = True
        ctl.type="chat"
        ctl.prompt_ref="openai_insurance_with_tool"
        return ctl

    def test_health(self):
        response = self.client.get(get_config().api_route + "/health")
        assert response.status_code == 200
        assert response.json() == {"Status": "Alive"}

    def test_version(self):
        response = self.client.get(get_config().api_route +"/version")
        assert response.status_code == 200
        print(response.json())
        assert response.json()["Version"] is not None

    def test_basic_general_chat_to_llm(self):
        ctl = self.build_ConversationControl()
        ctl.prompt_ref="default_prompt"
        ctl.query="You are an expert in AI, can you answer this question: What is the value proposition of LangChain?"
        response=self.client.post(get_config().api_route + "/c/generic_chat", json= ctl.model_dump())
        print(f"----> {response.json()}")
        assert response is not None
        assert response.status_code == 200

    def test_router_at_api_level_qa_basic(self):
        ctl = self.build_ConversationControl()
        ctl.query="You are an expert in AI, can you answer this question: What is the value proposition of LangChain?"
        ctl.type="qa"
        response = self.client.post("/api/v1/c/generic_cqa",
                        json= ctl.model_dump())
        print(response.json())
        assert response is not None
        assert response.status_code == 200
        print(response.json())


    def test_access_to_martin_client(self):
        """
        Verify the client is loaded by the agent executor
        """
        ctl = self.build_ConversationControl()
        ctl.query="what is the client record for id=1 ?"
        resp= self.client.post(get_config().api_route + "/c/generic_chat", json= ctl.model_dump())
        print(f"----> {resp.json()}")
        self.assertTrue(resp.json()["message"].find("David Martin") > 0 )

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