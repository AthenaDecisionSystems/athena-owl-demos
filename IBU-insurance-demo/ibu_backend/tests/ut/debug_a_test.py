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

    def define_conversation_control(self,query, aid: str = "ibu_agent"):
        cc = ConversationControl()
        cc.agent_id=aid
        cc.user_id="unit_test"
        cc.thread_id="1"
        cc.chat_history=[]
        cc.query=query
        cc.callWithVectorStore=False
        cc.callWithDecisionService=True
        return cc
    
    def pretty_print(self, response):
        lines = response.split('\n')
        for line in lines:
            print(line)

    def get_response_content(self, rep) -> str:
        print(f"\n@@@> {rep}")
        rep_dict= json.loads(rep)
        return rep_dict["messages"][0]["content"]

    def test_calling_agent(self):
        print("\n--- test to debug something specific")
        #query="What is the claim with an id 2?"
        query="Hi IBU, I am on the phone with one of my very impor tant customer. Her name is Sonya Smith. She has a problem with her claim 2 for their water damage. She told me that the carpet is expensive. She is surprised of the current coverage. Sonya finds this very disappointing. What should I answer? What is the next best action?"
      
        #cc=self.define_conversation_control(query, "WatsonxWithTools")
        cc=self.define_conversation_control(query,"ibu_agent2")
        rep = get_or_start_conversation(cc)
        print(f"\n\t--> {rep}")
        assert rep.messages[0].content
        cc.chat_history=rep.chat_history
        rep = get_or_start_conversation(cc)
        self.pretty_print(rep["messages"][0].content)



if __name__ == '__main__':
    unittest.main()