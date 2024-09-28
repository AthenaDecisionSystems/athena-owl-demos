"""
code to isolate a test if needed
"""
import unittest, sys, os
from dotenv import load_dotenv
load_dotenv()
# Order of the following code is important to make the tests working
os.environ["CONFIG_FILE"] = "./tests/ut/config/config.yaml"
module_path = "./src"
sys.path.append(os.path.abspath(module_path))

from athena.routers.dto_models import ConversationControl, ResponseControl
from athena.llm.conversations.conversation_mgr import get_or_start_conversation

class TestTestToDebugStuff(unittest.TestCase):

    def define_conversation_control(self,query, aid: str = "ibu_classify_query_agent"):
        cc = ConversationControl()
        cc.agent_id=aid
        cc.user_id="unit_test"
        cc.thread_id="1"
        cc.chat_history=[]
        cc.query=query
        return cc

    def test_calling_graph_agent(self):
        print("\n--- test_7_using_graph_agent_should_get_client_info to get client information from DB")
        query="What is the name of the client with an id 1?"
        cc=self.define_conversation_control(query, "ibu_agent")
        rep = get_or_start_conversation(cc)
        print(f"\n\t--> {rep}")
        self.assertNotEqual("I don't know", rep.messages[0].content)
        self.assertIn("David Martin", rep.messages[0].content)


if __name__ == '__main__':
    unittest.main()