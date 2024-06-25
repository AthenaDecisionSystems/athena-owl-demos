import unittest
import sys, os
module_path = "./src"
sys.path.append(os.path.abspath(module_path))
os.environ["CONFIG_FILE"] = "./tests/ut/config/config.yaml"
from dotenv import load_dotenv
load_dotenv()

from athena.routers.dto_models import ConversationControl
from athena.llm.conversations.conversation_mgr import get_or_start_conversation

class TestConversation(unittest.TestCase):
    
    def _validate_response(self, cc : ConversationControl):
        rep = get_or_start_conversation(cc)
        assert rep
        assert rep.message
        
        print(f"\n\nAssistant --> {rep}") 
        
       
        
        
    def test_conv_openai_base_graph_assistant(self):
        print("\n------- test_conversation to do tool calls on client by name")
        cc = ConversationControl()
        cc.assistant_id="ibu_assistant"
        cc.user_id="unit_test"
        cc.thread_id="3"
        cc.chat_history=[]
        cc.query="What is the credit score of Robert Smith using IBU loan database?"
        self._validate_response(cc)
        
if __name__ == '__main__':
    unittest.main()