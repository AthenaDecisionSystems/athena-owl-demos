import unittest
import sys, os
module_path = "./src"
sys.path.append(os.path.abspath(module_path))
os.environ["CONFIG_FILE"] = "./tests/ut/config/config.yaml"

from dotenv import load_dotenv, dotenv_values
from os.path import join, dirname
from pathlib import Path

#dotenv_path = join(Path(dirname(__file__)).parent.parent.parent.absolute(), '.env')
dotenv_path = join(Path(dirname(__file__)).absolute(), '../../../.env')
config = dotenv_values(dotenv_path)
for key in config:
    os.environ[key] = config[key]

#load_dotenv(dotenv_path)


from athena.routers.dto_models import ConversationControl
from athena.llm.conversations.conversation_mgr import get_or_start_conversation

class TestConversationWithTool(unittest.TestCase):
    """
    Validate conversation with tool to get news from search
    """    
    def test_conversation_that_fetches_customer_data(self):
        cc = ConversationControl()
        cc.agent_id="openai_chain_agent"
        cc.user_id="unit_test"
        cc.thread_id="1"
        cc.chat_history=[]
        cc.query="Give me the data of the customer with email pierre@acme.fr"
        rep = get_or_start_conversation(cc)
        assert rep
        assert rep.chat_history
        assert rep.messages
        print(f"agent --> {rep}")        
    

    """
    Validate conversation with tool to get news from search
    """    
    def test_conversation_that_performs_a_web_search(self):
        cc = ConversationControl()
        cc.agent_id="openai_chain_agent"
        cc.user_id="unit_test"
        cc.thread_id="1"
        cc.chat_history=[]
        cc.query="In October 2024, who is the prime minister of France?"
        rep = get_or_start_conversation(cc)
        assert rep
        assert rep.chat_history
        assert rep.messages
        print(f"agent --> {rep}")        
        
if __name__ == '__main__':
    unittest.main()