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

class TestIBUAssistant(unittest.TestCase):
    
    def test_get_info_query(self):
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
    
    def test_a_complaint_query(self):
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
         
    def _test_conv(self):
        cc = ConversationControl()
        cc.query="who is client with id 1?"
        cc.thread_id="thread_test"
        cc.assistant_id="ibu_assistant_LG"
        rep: Optional[ResponseControl]  = get_or_start_conversation(cc)
        print(rep)
        
if __name__ == '__main__':
    unittest.main()