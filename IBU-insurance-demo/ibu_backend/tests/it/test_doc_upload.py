import sys,os
sys.path.append('./src')

os.environ["CONFIG_FILE"] = "./tests/it/config/config.yaml"
from dotenv import load_dotenv
load_dotenv("../.env")
from athena.routers.documents import FileDescription
from fastapi.testclient import TestClient
import unittest
from athena.main import app

class TestDocumentMgt(unittest.TestCase):
    PATH_TO_DOCS="./tests/it/documents"
    @classmethod
    def setUpClass(self):
        self.client = TestClient(app)

    def test_upload_pdf(self):
        print("\n\t--- test_upload_pdf")
        fd= FileDescription(name="claim_complaint_rules", 
                            description="a set of rules to manage complaints", 
                            type="pdf",
                            file_name="ibu-claims-complaint-rules.pdf")
        files = {'myFile': (fd.file_name, open(self.PATH_TO_DOCS + "/" +  fd.file_name, 'rb'), "application/pdf")}

        rep=self.client.post('/api/v1/a/documents',json = fd.model_dump(),files=files) 
        assert rep
        assert rep.text
        print(rep)
        
    def test_upload_md(self):
        print("\n\t--- test_upload_md")
        fd= FileDescription(name="claim_complaint_rules", 
                            description="a set of rules to manage complaints", 
                            type="md",
                            file_name="ibu-claims-complaint-rules.md")
        files = {'myFile': (fd.file_name, open(self.PATH_TO_DOCS + "/" +  fd.file_name, 'rb'))}

        rep=self.client.post('/api/v1/a/documents',json = fd.model_dump(),files=files) 
        assert rep
        assert rep.text
        print(rep.text)
        
    def test_upload_html(self):
        print("\n\t--- test_upload_md")
        fd= FileDescription(name="claim_complaint_rules", 
                            description="a set of rules to manage complaints", 
                            type="html",
                            file_name="ibu-claims-complaint-rules.html")
        files = {'myFile': (fd.file_name, open(self.PATH_TO_DOCS + "/" +  fd.file_name, 'rb'))}

        rep=self.client.post('/api/v1/a/documents',json = fd.model_dump(),files=files) 
        assert rep
        assert rep.text
        print(rep.text)
        
if __name__ == '__main__':
    unittest.main()

