import unittest, sys, os
# Order of the following code is important to make the tests working
os.environ["CONFIG_FILE"] = "./tests/ut/config/config.yaml"
module_path = "./src"
sys.path.append(os.path.abspath(module_path))
from dotenv import load_dotenv
load_dotenv()

from athena.llm.assistants.assistant_mgr import get_assistant_manager
from athena.llm.conversations.conversation_mgr import get_or_start_conversation
from athena.routers.dto_models import ConversationControl, ResponseControl
from importlib import import_module

class TestIBUAssistant(unittest.TestCase):
    """
    Simulate a conversation flow using the ibu assistant
    """
    
    def test_calling_ibu_agent_tool_client(self):
        cc = ConversationControl()
        cc.query="who is client with id 1?"
        cc.thread_id="thread_test"
        cc.assistant_id="ibu_assistant"
        rep = get_or_start_conversation(cc)
        print(rep)
        
    def test_calling_ibu_assistant_claim_id_tool(self):
        cc = ConversationControl()
        cc.query="what is the state of the claim with id 1?"
        cc.thread_id="thread_test"
        cc.assistant_id="ibu_assistant"
        cc.user_id="test_user"
        rep = get_or_start_conversation(cc)
        print(rep)
        
if __name__ == '__main__':
    unittest.main()