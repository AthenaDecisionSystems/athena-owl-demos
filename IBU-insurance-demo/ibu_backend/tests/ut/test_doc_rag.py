import unittest, sys, os
# Order of the following code is important to make the tests working
os.environ["CONFIG_FILE"] = "./tests/ut/config/config.yaml"
module_path = "./src"
sys.path.append(os.path.abspath(module_path))
from dotenv import load_dotenv
load_dotenv()
import chromadb
from ibu.app_settings import get_config

from typing import Optional
from athena.itg.store.content_mgr import get_content_mgr, FileDescription

class TestIBUAssistant(unittest.TestCase):
    
    def test_1_upload_policy_document(self):
        print("test_1_upload_policy_document")
        service = get_content_mgr()
        fd=FileDescription()
        fd.name="Claims-complaint-rules"
        fd.file_name="IBU_policies_2.md"
        fd.file_base_uri="../scenarios"
        fd.type="md"
        fd.collection_name="test"
        rep=service.process_doc(fd,None) # content may be empty as it will be loaded from the file description url
        print(rep)
        assert rep
        assert "document Claims-complaint-rules processed" in rep
    
    def test_2_verify_collection_content(self):
        print("\n\n -- test_2_verify_collection_content")
        chroma_pah= get_config().owl_agent_vs_path
        client = chromadb.PersistentClient(path=chroma_pah)
        collection = client.get_collection(name="test")
        assert collection
        assert collection.count() > 0
        for c in client.list_collections():
            print(f"\nname = {c.name} number doc = {c.count()}")


    def test_3_similarity_search(self):
        print("\n\n -- test_3_similarity_search")
        service = get_content_mgr()
        results = service.search("test","what to do water damage inside individual house?",2)   # will return Documents
        print(results)
        assert results 
        for doc in  results:
            print(doc.page_content)

    
    def test_4_upload_pdf_document(self):
        print("\n\n -- test_4_upload_pdf_document")
        service = get_content_mgr()
        fd=FileDescription()
        fd.name="Claims-complaint-rules-pdf"
        fd.file_name="IBU_Policies.pdf"
        fd.file_base_uri="../scenarios"
        fd.type="pdf"
        fd.collection_name="test"
        rep=service.process_doc(fd,None) # content may be empty as it will be loaded from the file description url
        print(rep)
        assert rep

    def test_5_upload_html_document(self):
        print("\n\n -- test_5_upload_html_document")
        service = get_content_mgr()
        fd=FileDescription()
        fd.name="Claims-complaint-rules-html"
        fd.file_name="IBU_policies_2.html"
        fd.file_base_uri="../scenarios"
        fd.type="html"
        fd.collection_name="test"
        rep=service.process_doc(fd,None) # content may be empty as it will be loaded from the file description url
        print(rep)
        assert rep

    def test_7_clean(self):
        service = get_content_mgr()
        service.clear_collection("test")

if __name__ == '__main__':
    unittest.main()