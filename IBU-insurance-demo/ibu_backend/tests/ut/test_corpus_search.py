"""
Validate the IBU insurance agent with RAG seearch tool

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
from ibu.app_settings import get_config
from athena.itg.store.content_mgr import get_content_mgr, FileDescription

class Test_ibu_agent_rag(unittest.TestCase):
    """
    Validate the  rag tool with  IBU insurance agent
    """
    def define_conversation_control_for_test(self,query, aid: str = "ibu_agent"):
        cc = ConversationControl()
        cc.agent_id=aid
        cc.user_id="unit_test"
        cc.thread_id="1"
        cc.chat_history=[]
        cc.query=query
        return cc
    
    def upload_corpus(self):
        """
        Upload a document to be able to query on, using the collection defined in CONFIG_FILE
        """
        service = get_content_mgr()
        fd=FileDescription()
        fd.name="Claims-complaint-rules"
        fd.file_name="IBU_policies_2.md"
        fd.file_base_uri="../scenarios"
        fd.type="md"
        fd.collection_name=get_config().owl_agent_content_collection_name
        rep=service.process_doc(fd,None)
    
    def test_1_search_insurance_corpus(self):
        print("\n--- test_1_search_insurance_corpus")
        print("\n -1- upload doc in collection")
        self.upload_corpus()
        query="what coverage is in the IBU insurance policy for water damage?"
        print("\n -2- query {query} using the agent and rag tool\n\n")
        cc=self.define_conversation_control_for_test(query,"ibu_agent")
        rep = get_or_start_conversation(cc)
        print(f"\n\t--> {rep}")
        assert "limited to 45% of the repair cost" in rep.messages[0].content.lower()
        service = get_content_mgr()
        service.clear_collection(get_config().owl_agent_content_collection_name)
