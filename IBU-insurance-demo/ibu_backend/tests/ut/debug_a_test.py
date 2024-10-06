"""
code to isolate a test if needed
"""
import unittest, sys, os, json
from dotenv import load_dotenv
load_dotenv()
# Order of the following code is important to make the tests working
os.environ["CONFIG_FILE"] = "./tests/ut/config/config.yaml"
module_path = "./src"
sys.path.append(os.path.abspath(module_path))

from athena.routers.dto_models import ConversationControl, ResponseControl
from athena.llm.conversations.conversation_mgr import get_or_start_conversation, get_conversation_trace_given_thread_id

class TestTestToDebugStuff(unittest.TestCase):

    def define_conversation_control(self,query, aid: str = "ibu_classify_query_agent"):
        cc = ConversationControl()
        cc.agent_id=aid
        cc.user_id="unit_test"
        cc.thread_id="1"
        cc.chat_history=[]
        cc.query=query
        return cc
    
    def get_response_content(self, rep) -> str:
        print(f"\n@@@> {rep}")
        rep_dict= json.loads(rep)
        return rep_dict["messages"][0]["content"]

    def test_calling_graph_agent(self):
        print("\n--- test_10 get_claim_status as a complain")
        #query="My name is Sonya Smith, I want to know the status of my current claim?"
        #query="Hi IBU, I am on the phone with one of my very important customer. Her name is Sonya Smith. She has a problem with her claim 2 for their water damage. She told me that the carpet is expensive. She is surprised of the current coverage. Sonya finds this very disappointing. What would be the next best action?"
        query="asdfdsg grtggfdgre dcfs"
        cc=self.define_conversation_control(query, "ibu_agent")
        rep = get_or_start_conversation(cc)
        print(f"\n\t--> {rep}")
        assert rep.messages[0].content
        assert "didn't understand" in rep.messages[0].content

if __name__ == '__main__':
    unittest.main()