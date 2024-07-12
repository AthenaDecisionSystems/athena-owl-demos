"""
Validate the IBU insurance assistant implemented with LangGraph

Copyright 2024 Athena Decision Systems
@author Jerome Boyer

"""
import unittest
import sys
import os
from dotenv import load_dotenv
load_dotenv()

# Order of the following code is important to make the tests working
os.environ["CONFIG_FILE"] = "./tests/ut/config/config.yaml"
module_path = "./src"
sys.path.append(os.path.abspath(module_path))


from typing import Optional
from athena.routers.dto_models import ConversationControl, ResponseControl
from athena.llm.conversations.conversation_mgr import get_or_start_conversation
from athena.llm.agents.agent_mgr import get_agent_manager, OwlAgentEntity
from athena.itg.store.content_mgr import get_content_mgr, FileDescription

class Test_ibu_assistant_langgraph(unittest.TestCase):
    """
    Validate the IBU insurance assistant implemented with LangGraph
    """
         
    def _test_1_verify_get_client_tool(self):
        print("\n--- test_verify_get_client_tool to verify tool calling")
        cc = ConversationControl()
        cc.query="who is client with id 1?"
        cc.thread_id="thread_test"
        cc.assistant_id="ibu_assistant_lg"
        rep: Optional[ResponseControl]  = get_or_start_conversation(cc)
        print(rep)
        assert "Martin" in rep.message # type: ignore
    
    def _test_2_verify_get_claim_tool(self):
        print("\n--- test_verify_get_claim_tool to verify tool calling")
        cc = ConversationControl()
        cc.query="what is the claim with id 2?"
        cc.thread_id="2"
        cc.assistant_id="ibu_assistant_lg"
        rep: Optional[ResponseControl]  = get_or_start_conversation(cc)
        print(rep)
        assert "water damage" in rep.message # type: ignore
    
    def test_information_about_insurance(self):
        print("\n--- test_information_about_insurance to verify tool calling")
        cc = ConversationControl()
        cc.callWithVectorStore= True
        cc.query="my name is Sonya Smith, I would like to get a status of my insurance policy"
        cc.thread_id="2"
        cc.assistant_id="ibu_assistant_lg"
        rep: Optional[ResponseControl]  = get_or_start_conversation(cc)
        print(rep)
        assert "CLTV percentile is 62" in rep.message   # RAG adds hallucination
        
    def _test_verify_call_odm_tool(self):
        print("\n--- test_verify_call_odm_tool to verify tool calling")
        cc = ConversationControl()
        
        cc.query="""My name is Sonya Smith, I have problem with my claim with ID=2 for my water damage, \
            my carpet is expensive, I'm surprise of the current coverage, very disappointing!
            """
        cc.thread_id="2"
        cc.assistant_id="ibu_assistant_lg"
        rep: Optional[ResponseControl]  = get_or_start_conversation(cc)
        print(rep)
        #assert "In Process Verified" in rep.message # type: ignore

if __name__ == '__main__':
    unittest.main()