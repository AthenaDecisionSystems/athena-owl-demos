import unittest, sys, os
# Order of the following code is important to make the tests working
os.environ["CONFIG_FILE"] = "./tests/ut/config/config.yaml"
module_path = "./src"
sys.path.append(os.path.abspath(module_path))
from dotenv import load_dotenv
load_dotenv()

from typing import Optional
from athena.itg.store.content_mgr import get_content_mgr, FileDescription

class TestIBUAssistant(unittest.TestCase):
    
    def test_1_upload_policy_document(self):
        service = get_content_mgr()
        fd=FileDescription()
        fd.name="Claims-complaint-rules"
        fd.file_name="IBU_policies_2.md"
        fd.file_base_uri="../scenarios"
        fd.type="md"
        rep=service.process_doc(fd,None)
        print(rep)
        assert "document Claims-complaint-rules processed" in rep
        
    def test_2_similarity_search(self):
        service = get_content_mgr()
        results = service.search("what is insurance policy 41?")   # will return Documents
        print(results[0])
        assert "complaint about the level of claim reimbursement" in results[0].page_content

if __name__ == '__main__':
    unittest.main()