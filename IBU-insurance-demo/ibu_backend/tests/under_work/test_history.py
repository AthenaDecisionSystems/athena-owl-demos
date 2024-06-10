from fastapi.testclient import TestClient
import unittest
from dotenv import load_dotenv
import sys,os
sys.path.append('./src')
from athena.main import app
from athena import  dependencies
from athena.routers.dto_models import ChatRecord, ConversationControl

"""
Test the app at the api level using FastAPI test client, and configuration for tests.
Run from folder above tests.

pytest -s tests/it/test_app_api.py
"""
class TestAppApi(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):
        os.environ["CONFIG_FILE"]="src/athena/config/config.yaml"
        config = dependencies.get_config()
        config["owl_glossary_path"]= "./src/athena/config/glossary.json"
        config["owl_prompts_path"]="./src/athena/config/prompts.json"
        config["owl_env_path"]= ".env"
        load_dotenv(dotenv_path=config["owl_env_path"])
        self.client = TestClient(app)
        print("init test done")

    def test_basic_history(self):
        """
        Verify LLM is taking into account history
        """
        ctl = ConversationControl()
        ctl.callWithVectorStore = False
        ctl.callWithDecisionService = False
        ctl.type="chat"
        ctl.query="what is my date of birth?"
        ctl.prompt_ref="default_prompt"
        ctl.chat_history=[ChatRecord(role="human",content= "Hi I am bob lazard, I am born on June 27 1902"), 
                          ChatRecord(role="assistant", content="Hi how can I help you?")]
        resp=self.client.post("/c/generic_chat", json= ctl.model_dump())
        print(f"----> {resp.json()}")
        self.assertTrue(resp.json()["message"].find("1902") > 0 )

