import unittest, sys, os
# Order of the following code is important to make the tests working
os.environ["CONFIG_FILE"] = "./tests/ut/config/config.yaml"
module_path = "./src"
sys.path.append(os.path.abspath(module_path))
from dotenv import load_dotenv
load_dotenv()

from typing import Optional
from athena.routers.dto_models import ConversationControl, ResponseControl
from athena.llm.conversations.conversation_mgr import get_or_start_conversation
from athena.llm.agents.agent_mgr import get_agent_manager, OwlAgentEntity
from athena.itg.store.content_mgr import get_content_mgr, FileDescription

class TestIBUAssistant(unittest.TestCase):
    
    def _test_upload_policy_document(self):
        service = get_content_mgr()
        fd=FileDescription()
        fd.name="Claims-complaint-rules"
        fd.file_name="IBU_policies_2.md"
        fd.file_base_uri="../scenarios"
        fd.type="md"
        rep=service.process_doc(fd,None)
        print(rep)
        assert rep
        
    def _test_get_info_query(self):
        print("test_get_info_query to classify the query")
        query="My name is Sonya Smith, I want to get information about my insurance policy. "
        mgr = get_agent_manager()
        oae: Optional[OwlAgentEntity] = mgr.get_agent_by_id("ibu_classify_query_agent")
        if oae is None:
            raise ValueError("ibu_classify_query_agent agent not found")
        agent = mgr.build_agent(oae.agent_id,"en")
        assert agent
        rep = agent.invoke({"input": query, "chat_history": []} )
        print(rep)
        assert "INFORMATION" in rep
    
    def _test_a_complaint_query(self):
        print("test_a_complaint_query to classify the query")
        query="My name is Sonya Smith, I have problem with my claim 2 for my water damage, I still did not get a status from you since 2 months  "
        mgr = get_agent_manager()
        oae: Optional[OwlAgentEntity] = mgr.get_agent_by_id("ibu_classify_query_agent")
        if oae is None:
            raise ValueError("ibu_classify_query_agent agent not found")
        agent = mgr.build_agent(oae.agent_id,"en")
        assert agent
        rep = agent.invoke({"input": query, "chat_history": []} )
        print(rep)
        assert "COMPLAINT" in rep
         
    def _test_verify_get_client_tool(self):
        print("test_verify_get_client_tool to verify tool calling")
        cc = ConversationControl()
        cc.query="who is client with id 1?"
        cc.thread_id="thread_test"
        cc.assistant_id="ibu_assistant"
        rep: Optional[ResponseControl]  = get_or_start_conversation(cc)
        print(rep)
        assert "Martin" in rep.message # type: ignore
    
    def _test_verify_get_claim_tool(self):
        print("test_verify_get_claim_tool to verify tool calling")
        cc = ConversationControl()
        cc.query="what is the claim with id 2?"
        cc.thread_id="2"
        cc.assistant_id="ibu_assistant"
        rep: Optional[ResponseControl]  = get_or_start_conversation(cc)
        print(rep)
        assert "In Process Verified" in rep.message # type: ignore
    
    def test_information_about_insurance(self):
        print("test_information_about_insurance to verify tool calling")
        cc = ConversationControl()
        cc.callWithVectorStore= True
        cc.query="my name is Sonya Smith, I would like to get a status of my insurance policy"
        cc.thread_id="2"
        cc.assistant_id="ibu_assistant_LG"
        rep: Optional[ResponseControl]  = get_or_start_conversation(cc)
        print(rep)
        
    def _test_verify_call_odm_tool(self):
        print("test_verify_call_odm_tool to verify tool calling")
        cc = ConversationControl()
        
        cc.query="My name is Sonya Smith, I have problem with my claim 2 for my water damage, my carpet is expensive, I'm surprise of the current coverage, very disappointing"
        cc.thread_id="2"
        cc.assistant_id="ibu_assistant_LG"
        rep: Optional[ResponseControl]  = get_or_start_conversation(cc)
        print(rep)
        #assert "In Process Verified" in rep.message # type: ignore

if __name__ == '__main__':
    unittest.main()