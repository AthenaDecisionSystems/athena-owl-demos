import unittest
import sys, os
module_path = "./src"
sys.path.append(os.path.abspath(module_path))
os.environ["CONFIG_FILE"] = "./tests/ut/config/config.yaml"
from dotenv import load_dotenv
load_dotenv()

from athena.routers.dto_models import ConversationControl
from athena.llm.conversations.conversation_mgr import get_or_start_conversation

class TestSwappingagent(unittest.TestCase):

    def test_conv_to_get_a_loan_demonstrating_hallucination(self):
        """Keep the same thread id"""
        print("\n------- test_conv_to_get_a_loan_demonstrating_hallucination as this agent has no loan decision service")
        cc = ConversationControl()
        cc.agent_id="ibu_agent_limited"
        cc.user_id="unit_test"
        cc.thread_id="4"
        cc.chat_history=[]
        cc.query="One of our client Robert Smith wants a loan for $1,000,000 for a duration of 60 months with a yearly repayment of $60,000 do we approve it?"
        rep = get_or_start_conversation(cc)
        assert rep
        assert rep.messages
        print(f"\n\nagent --> {rep}")
        cc.agent_id="ibu_agent"
        cc.thread_id="4"
        rep = get_or_start_conversation(cc)
        assert rep
        assert rep.messages
        print(f"\n\nagent --> {rep}")
       
        
if __name__ == '__main__':
    unittest.main()