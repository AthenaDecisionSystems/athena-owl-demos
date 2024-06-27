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
        
    def _test_conv_openai_base_assistant(self):
        print("\n------- test_conversation to do tool calls on client by name")
        cc = ConversationControl()
        cc.assistant_id="ibu_assistant"
        cc.user_id="unit_test"
        cc.thread_id="3"
        cc.chat_history=[]
        cc.query="What is the credit score of Robert Smith using IBU loan database?"
        rep = get_or_start_conversation(cc)
        assert rep
        assert rep.message
        assert "150" in rep.message
        assert "credit score" in rep.message
        print(f"\n\nAssistant --> {rep}") 
        """Example of response without decision service:
        Based on the information available, Robert Smith has a yearly income of $140,000 and a credit score of 150. 
        However, he had a bankruptcy filing in 2018. \n\nBefore making a decision on approving the loan, we need to 
        consider the bankruptcy filing and its impact on his creditworthiness. Would you like me to proceed with 
        evaluating the loan application further?
        """
    
    def test_conv_to_get_a_loan(self):
        print("\n------- test_conversation to do tool calls on get loan decision")
        cc = ConversationControl()
        cc.assistant_id="ibu_assistant"
        cc.user_id="unit_test"
        cc.thread_id="3"
        cc.chat_history=[]
        cc.query="One of our client Robert Smith wants a loan for $500,000 for a duration of 60 months with a yearly repayment of $60,000 do we approve it?"
        rep = get_or_start_conversation(cc)
        assert rep
        assert rep.message
        print(f"\n\nAssistant --> {rep}") 
        assert ("has not been approved" in rep.message or "has been declined" in rep.message or "not approved" in rep.message)
        
    def test_conv_to_get_a_loan_approved(self):
        print("\n------- test_conversation to do tool calls on get loan decision")
        cc = ConversationControl()
        cc.assistant_id="ibu_assistant"
        cc.user_id="unit_test"
        cc.thread_id="3"
        cc.chat_history=[]
        cc.query="One of our client Jean Martin wants a loan for $300,000 for a duration of 180 months and a yearly repayment of $40,000 do we approve it?"
        rep = get_or_start_conversation(cc)
        assert rep
        assert rep.message
        print(f"\n\nAssistant --> {rep}") 
        assert "has been approved" in rep.message

    def test_conv_to_get_a_loan_demonstrating_hallucination(self):
        print("\n------- test_conv_to_get_a_loan_demonstrating_hallucination as this assistant has no loan decision service")
        cc = ConversationControl()
        cc.assistant_id="ibu_assistant_limited"
        cc.user_id="unit_test"
        cc.thread_id="4"
        cc.chat_history=[]
        cc.query="One of our client Robert Smith wants a loan for $500,000 for a duration of 60 months with a yearly repayment of $60,000 do we approve it?"
        rep = get_or_start_conversation(cc)
        assert rep
        assert rep.message
        print(f"\n\nAssistant --> {rep}") 
       
        
if __name__ == '__main__':
    unittest.main()