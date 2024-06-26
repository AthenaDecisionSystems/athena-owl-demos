import unittest
import sys,os
os.environ["CONFIG_FILE"] = "./tests/ut/config/config.yaml"
from dotenv import load_dotenv
load_dotenv()
sys.path.append('./src')
import requests
from ibu.app_settings import  get_config
from athena.routers.dto_models import ConversationControl,ResponseControl


"""
Test the app at the api level using htpp client

pytest -s tests/it/test_conversation_api.py

Goals: 
"""
class TestAssistantsAPIs(unittest.TestCase):
    
       

    def build_ConversationControl(self):
        ctl = ConversationControl()
        ctl.callWithVectorStore = False
        ctl.callWithDecisionService = False
        ctl.type="chat"
        ctl.assistant_id="ibu_assistant"
        ctl.user_id="test_user"
        ctl.thread_id="1"
        return ctl
    
    def test_tool_calling_get_client(self):
        ctl = self.build_ConversationControl()
        ctl.query="What is the credit score of Robert Smith as future borrower?"
        response=requests.post(get_config().api_route + "/c/generic_chat", json= ctl.model_dump())
        assert response
        assert response.status_code == 200
        print(f"\n--it--> {response.content}")
        
if __name__ == '__main__':
    unittest.main()