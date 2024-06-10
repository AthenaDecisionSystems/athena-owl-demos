
import unittest
import sys,os
sys.path.append('./src')
os.environ["CONFIG_FILE"] = "./tests/it/config/config.yaml"
from dotenv import load_dotenv
load_dotenv("./.env")

from ibu.main import app
from athena.routers.dto_models import ConversationControl
from fastapi.testclient import TestClient
from athena.app_settings import  get_config
"""
Test the app at the api level using FastAPI test client, and configuration for tests.
Run from folder above tests.

pytest -s tests/it/test_app_api.py
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
        ctl.type="qa"
        ctl.prompt_ref="openai_insurance_with_tool"
        return ctl

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
    

   