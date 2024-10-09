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
from athena.itg.store.content_mgr import get_content_mgr, FileDescription

FILE_TO_UPLOAD="IBU_policies_2.html"

class TestIbuScenario(unittest.TestCase):

    def define_conversation_control(self,query, aid: str = "ibu_agent"):
        cc = ConversationControl()
        cc.agent_id=aid
        cc.user_id="unit_test"
        cc.thread_id="1"
        cc.chat_history=[]
        cc.query=query
        cc.callWithVectorStore=True
        return cc
    
    def get_response_content(self, rep) -> str:
        print(f"\n@@@> {rep}")
        rep_dict= json.loads(rep)
        return rep_dict["messages"][0]["content"]

    def test_scenario_1(self):
        print("\n--- Say hello")
        query="hello"
        cc=self.define_conversation_control(query, "ibu_agent")
        rep = get_or_start_conversation(cc)
        print(f"\n\t--> {rep}")
        assert rep.messages[0].content
        print("\n\n -- upload_html_document")
        service = get_content_mgr()
        fd=FileDescription()
        fd.name="Claims-complaint-rules-html"
        fd.file_name=FILE_TO_UPLOAD
        fd.file_base_uri="../scenarios"
        fd.type="html"
        fd.collection_name="test"
        rep=service.process_doc(fd,None) # content may be empty as it will be loaded from the file description url
     

        query="""
*I received this email from my customer. What should I answer?*
**From**: Sonya Smith (sonya.smith@thecure.org)
**To**: support@ibuinsurance.com
**Subject**: Covering my carpet cleaning
Dear IBU,
During the recent water leak at my house (cf claim 2), my expensive Moroccan carpet was damaged by the water.\xa0 You told me that this damage is not covered by my policy.  I’m very disappointed.  It will be expensive to get it cleaned.\xa0 What do you propose?
Thank you!
Yours,
**Sonya Smith**
"""
        cc=self.define_conversation_control(query, "ibu_agent")
        rep = get_or_start_conversation(cc)
        print(f"\n\t--> {rep}")

if __name__ == '__main__':
    unittest.main()