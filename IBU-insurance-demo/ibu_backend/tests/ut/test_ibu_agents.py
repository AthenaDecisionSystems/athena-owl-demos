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



class Test_ibu_agent(unittest.TestCase):
    """
    Validate the IBU insurance agents
    """
    def define_conversation_control(self,query, aid: str = "ibu_classify_query_agent"):
        cc = ConversationControl()
        cc.agent_id=aid
        cc.user_id="unit_test"
        cc.thread_id="1"
        cc.chat_history=[]
        cc.query=query
        return cc

    def test_1_classify_agent_for_info_query(self):
        print("\n--- test_get_info_query to classify the query")
        query="My name is Sonya Smith, I want to get information about my insurance policy. "
        cc=self.define_conversation_control(query)
        rep = get_or_start_conversation(cc)
        print(f"\n\t--> {rep}")
        assert "Information" in rep.messages[0].content
    
    def test_2_classify_agent_for_complaint_query(self):
        print("\n--- test_a_complaint_query to classify the query to complaint")
        query="My name is Sonya Smith, I have problem with my claim 2 for my water damage, I still did not get a status from you since 2 months  "
        cc=self.define_conversation_control(query)
        rep = get_or_start_conversation(cc)
        print(f"\n\t--> {rep}")
        assert "Complaint" in rep.messages[0].content

         
    
    def test_3_information_agent(self):
        """When the branch is in the information node, generic query should get results from Tavily, but insurance should get claim by id"""
        print("\n--- test_3_information_agent to get general response from web search")
        query="What is the weather today in San Francisco?"
        cc=self.define_conversation_control(query, "ibu_tool_rag_agent_limited")
        rep = get_or_start_conversation(cc)
        print(f"\n\t--> {rep}")
        assert "I don't know" in rep.messages[0].content
        
    def test_4_information_agent_on_insurance_client(self):
        """When the branch is in the information node, query about insurance domain should get claim by id, client by name..."""
        print("\n--- test_4_information_agent_on_insurance_client to get client information from DB")
        query="What is the name of the client with an id 2?"
        cc=self.define_conversation_control(query, "ibu_tool_rag_agent_limited")
        rep = get_or_start_conversation(cc)
        print(f"\n\t--> {rep}")
        self.assertNotEqual("I don't know", rep.messages[0].content)
        self.assertIn("Sonya Smith", rep.messages[0].content)
        
    def test_5_information_agent_on_insurance_claim(self):
        """When the branch is in the information node, query about insurance domain should get claim by id, client by name..."""
        print("\n--- test_35_information_agent_on_insurance_claim to get claim information from DB")
        query="What is the status of the claim with the id 2?"
        cc=self.define_conversation_control(query, "ibu_tool_rag_agent_limited")
        rep = get_or_start_conversation(cc)
        print(f"\n\t--> {rep}")
        self.assertNotEqual("I don't know", rep.messages[0].content)
        self.assertIn("claim with ID 2 is currently", rep.messages[0].content)

    
    def test_6_information_from_rag_collection(self):
        """When the branch is in the information node, query about insurance domain should get claim by id, client by name..."""
        print("\n--- test_6_information_from_rag_collection to get business policy definition")
        query="what is insurance policy 41?"
        cc=self.define_conversation_control(query, "ibu_tool_rag_agent_limited")
        rep = get_or_start_conversation(cc)
        print(f"\n\t--> {rep}")
        self.assertNotEqual("I don't know", rep.messages[0].content)

    def test_7_using_graph_agent_should_get_client_info(self):
        print("\n--- test_7_using_graph_agent_should_get_client_info to get client information from DB")
        query="What is the name of the client with an id 1?"
        cc=self.define_conversation_control(query, "ibu_agent_limited")
        rep = get_or_start_conversation(cc)
        print(f"\n\t--> {rep}")
        self.assertNotEqual("I don't know", rep.messages[0].content)
        self.assertIn("David Martin", rep.messages[0].content)

    def test_8_using_graph_agent_should_get_claim_info(self):
        print("\n--- test_8_using_graph_agent_should_get_claim_info to get client information from DB")
        query="what is the claim with id 2?"
        cc=self.define_conversation_control(query, "ibu_agent_limited")
        rep = get_or_start_conversation(cc)
        print(f"\n\t--> {rep}")
        self.assertIn("water damage", rep.messages[0].content)

    def test_9_using_graph_agent_should_get_policy_info_from_user_name(self):
        print("\n--- test_9_using_graph_agent_should_get_policy_info_from_user_name to get client information from DB")
        query="my name is Sonya Smith, I would like to get a status of my insurance policy"  
        cc=self.define_conversation_control(query, "ibu_agent_limited")
        rep = get_or_start_conversation(cc)
        print(f"\n\t--> {rep}")
        self.assertIn("insurance policy", rep.messages[0].content)

if __name__ == '__main__':
    unittest.main()