"""
Validate the IBU insurance agent

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

class Test_ibu_agent(unittest.TestCase):
    """
    Validate the IBU insurance agents
    """
    
    def test_1_classify_agent_for_info_query(self):
        print("\n--- test_get_info_query to classify the query")
        query="My name is Sonya Smith, I want to get information about my insurance policy. "
        mgr = get_agent_manager()
        oae: Optional[OwlAgentEntity] = mgr.get_agent_by_id("ibu_classify_query_agent")
        if oae is None:
            raise ValueError("ibu_classify_query_agent agent not found")
        agent = mgr.build_agent(oae.agent_id,"en")
        assert agent
        rep = agent.invoke({"question": query} )
        print(rep)
        assert "information" in rep.next_task
    
    def test_2_classify_agent_for_complaint_query(self):
        print("\n--- test_a_complaint_query to classify the query to complaint")
        query="My name is Sonya Smith, I have problem with my claim 2 for my water damage, I still did not get a status from you since 2 months  "
        mgr = get_agent_manager()
        oae: Optional[OwlAgentEntity] = mgr.get_agent_by_id("ibu_classify_query_agent")
        if oae is None:
            raise ValueError("ibu_classify_query_agent agent not found")
        agent = mgr.build_agent(oae.agent_id,"en")
        assert agent
        rep = agent.invoke({"question": query} )
        print(rep)
        assert "complaint" in rep.next_task
         
    
    def test_3_information_agent(self):
        """When the branch is in the information node, generic query should get results from Tavily, but insurance should get claim by id"""
        print("\n--- test_3_information_agent to get general response from web search")
        query="What is the weather today in San Francisco?"
        mgr = get_agent_manager()
        oae: Optional[OwlAgentEntity] = mgr.get_agent_by_id("ibu_tool_rag_agent_limited")
        if oae is None:
            raise ValueError("ibu_classify_query_agent agent not found")
        agent = mgr.build_agent(oae.agent_id,"en")
        assert agent
        print(agent.get_tools())
        rep = agent.invoke({"question": query, "context": ""} )
        print(rep["output"])
        self.assertNotEqual("I don't know", rep["output"])
        
    def test_4_information_agent_on_insurance_client(self):
        """When the branch is in the information node, query about insurance domain should get claim by id, client by name..."""
        print("\n--- test_4_information_agent_on_insurance_client to get client information from DB")
        query="What is the name of the client with an id 2?"
        mgr = get_agent_manager()
        oae: Optional[OwlAgentEntity] = mgr.get_agent_by_id("ibu_tool_rag_agent_limited")
        agent = mgr.build_agent(oae.agent_id,"en")
        rep = agent.invoke({"question": query, "context": ""} )
        print(rep["output"])
        self.assertNotEqual("I don't know", rep["output"])
        self.assertIn("Sonya Smith", rep["output"])
        
    def test_5_information_agent_on_insurance_claim(self):
        """When the branch is in the information node, query about insurance domain should get claim by id, client by name..."""
        print("\n--- test_35_information_agent_on_insurance_claim to get claim information from DB")
        query="What is the status of the claim with the id 2?"
        mgr = get_agent_manager()
        oae: Optional[OwlAgentEntity] = mgr.get_agent_by_id("ibu_tool_rag_agent_limited")
        agent = mgr.build_agent(oae.agent_id,"en")
        rep = agent.invoke({"question": query, "context": ""} )
        print(rep["output"])
        self.assertNotEqual("I don't know", rep["output"])
        self.assertIn("claim with ID 2 is currently", rep["output"])

    
    def test_6_information_from_rag_collection(self):
        """When the branch is in the information node, query about insurance domain should get claim by id, client by name..."""
        print("\n--- test_6_information_from_rag_collection to get business policy definition")
        query="what is insurance policy 41?"
        mgr = get_agent_manager()
        oae: Optional[OwlAgentEntity] = mgr.get_agent_by_id("ibu_tool_rag_agent_limited")
        agent = mgr.build_agent(oae.agent_id,"en")
        rep = agent.invoke({"question": query, "context": ""} )
        print(rep["output"])
        self.assertNotEqual("I don't know", rep["output"])

        
if __name__ == '__main__':
    unittest.main()