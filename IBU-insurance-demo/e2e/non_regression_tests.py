"""
a bunch of calls to the backend servers to validate the major functions
"""
from pydantic import BaseModel
import unittest
import requests
from typing import Optional
IBU_BASE_URL="http://localhost:8002/api/v1"
AGENT_REF="ibu_agent"

class OwlAgent(BaseModel):
    """
    Entity definition to persist data about a OwlAgent
    """
    agent_id: str = ""
    name: str = ""
    description: Optional[str] = None
    modelName: str = ""
    modelClassName: Optional[str] = None
    runner_class_name: Optional[str] = "athena.llm.agents.agent_mgr.OwlAgentAbstractRunner"
    prompt_ref:  Optional[str] = None
    temperature: int = 0  # between 0 to 100 and will be converted depending of te LLM
    top_k: int = 1
    top_p: int = 1
    tools: list[str] = []
  
class TestHappyPathScenario(unittest.TestCase):

    def test_1_verify_health(self):
        print("\n--> Validate the Web App is Alive\n")
        rep = requests.get(IBU_BASE_URL + "/health", timeout = 10).content.decode()
        assert "Alive" in rep
        print(f"@@@> {rep} -> good!")

    def test_2_verify_version(self):
        print("\n--> Validate the Web App version\n")
        rep = requests.get(IBU_BASE_URL + "/version", timeout = 10).content.decode()
        assert "Version" in rep
        print(f"@@@> {rep} -> good!")

    def test_2_reload(self):
        print("\n--> Validate the Web App reload\n")
        rep = requests.put(IBU_BASE_URL + "/reload", timeout = 10).content.decode()
        print(f"@@@> {rep} -> good!")
        assert "Reload configuration done" in rep

    def test_3_validate_ibu_tools(self):
        print("\n--> Get IBU tool entity\n")
        tool_id = "ibu_claim_by_id"
        rep = requests.get(IBU_BASE_URL + "/a/tools/"+tool_id, timeout=10).content.decode()
        print(f"@@@> {rep}")
        assert "get insurance claim information" in rep
        tool_id = "ibu_client_by_id"
        rep = requests.get(IBU_BASE_URL + "/a/tools/"+tool_id, timeout=10).content.decode()
        print(f"@@@> {rep}")
        assert "insurance client information" in rep
        tool_id="ibu_claim_status_by_user_name"
        rep = requests.get(IBU_BASE_URL + "/a/tools/"+tool_id, timeout=10).content.decode()
        print(f"@@@> {rep}")
        assert "last status for the claim" in rep

    def test_4_validate_prompts(self):
        print("\n--> Get IBU prompts\n")
        prompt_id="openai_insurance_with_tool"
        rep = requests.get(IBU_BASE_URL + "/a/prompts/"+prompt_id+"/en", timeout=10).content.decode()
        print(f"@@@> {rep}")
        assert "assist a customer service" in rep

    def test_5_validate_ibu_agent(self):
        print("\n--> Get IBU agent entity\n")
        resp = requests.get(IBU_BASE_URL + "/a/agents/" + AGENT_REF, timeout=10)
        a_str= resp.content.decode()
        print(f"@@@> {a_str}")
        ae = OwlAgent.model_validate_json(json_data=a_str)
        print(f"@@@> {ae}")
        assert ae


 

    def test_6_access_to_data_mgr(self):
        print("\n--> Call to get an insured person to validate the data management service works\n")
        rep = requests.get("http://localhost:8080/repository/clients/search/Smith", timeout = 10).content.decode() 
        assert "Sonya" in rep
        print(f"@@@> {rep}  -> good")

    def test_7_upload_md_insurance_doc(self):
        print("\n--> Upload MD document to vector store\n")
        fname="../scenarios/Property and Casualty Insurance - Retention Rules.md"
        f = open(fname, "rb")
        files = {'myFile' :  f }
        rep = requests.post(IBU_BASE_URL + "/a/documents?name=IBU_policies-complaint&description=The%20rules%20about%20claim%20complaint%20management&type=md&collection_name=ibutest", files=files, timeout = 10).content.decode()
        print(f"\n@@@> {rep}")
        assert "document IBU_policies-complaint processed" in rep
        print("Validate there is some similarity search working")
        rep = requests.get(IBU_BASE_URL + "/a/documents/ibutest/policy%2041/3")
        print(f"\n@@@> {rep}")
    
    def test_8_perform_general_knowledge_query_legacy(self):
        print("\n--> Validate Basic Query to LLM\n")
        data='{  "locale": "en",\
          "query": "can you give me some information about Athena Decision Systems?",\
          "agent_id": "' + AGENT_REF + '",  \
          "user_id" : "remote_test", \
          "chat_history": [],\
          "thread_id" : "1" \
        }'
        rep = requests.post(IBU_BASE_URL + "/c/generic_chat", data=data, headers = {"Content-Type": "application/json"}, timeout = 10).content.decode()
        print(f"@@@> {rep}")
        assert rep
  
    def test_9_get_best_action_using_LLM(self):
        print("\n--> Get claim - client best action using agent with langgraph\n")
        data='{ "locale": "en",\
                  "query": "One of our client, Sonya Smith, has a problem with her claim with the id=2 for water damage, her carpet is expensive, she is surprise by the current coverage, very disappointed?",\
                  "chat_history": [],\
                  "agent_id": "' + AGENT_REF + '",  \
                  "callWithVectorStore": false, \
                  "callWithDecisionService": true, \
                  "user_id" : "remote_test"\
                   "thread_id" : "3" 
              }'
        print(data)
        rep = requests.post(IBU_BASE_URL + "/c/generic_chat", data=data, headers = {"Content-Type": "application/json"}, timeout = 10).content.decode()
        print(f"\n@@@> {rep}")

    def test_10_another_query(self):
        query="""
        Hi IBU, I am on the phone with one of my very important customer. Her name is Sonya Smith. She has a problem with her claim 2 
        for their water damage. She told me that the carpet is expensive. She is surprised of the current coverage. 
        Sonya finds this very disappointing. What would be the next best action?"""
        data='{ "locale": "en",\
                  "query": ' + query + '", \
                  "chat_history": [],\
                  "agent_id": "' + AGENT_REF + '",  \
                   "callWithVectorStore": false, \
                  "callWithDecisionService": true, \
                  "user_id" : "remote_test", \
                  "thread_id" : "3" \
              }'
        rep = requests.post(IBU_BASE_URL + "/c/generic_chat", data=data, headers = {"Content-Type": "application/json"}, timeout = 10).content.decode()
        print(f"\n@@@> {rep}")

if __name__ == "__main__":
    print("################ Non Regression Tests ##############")
    unittest.main()
  







