"""
a bunch of calls to the backend servers to validate the major functions
"""
from pydantic import BaseModel

import requests

IBU_BASE_URL="http://localhost:8000/api/v1"

class OwlAssistantEntity(BaseModel):
    """
    Entity to persist data about a OwlAssistant
    """
    assistant_id: str = "default_assistant"
    name: str = "default_assistant"
    description: str = "A default assistant to do simple LLM calls"
    class_name : str = "athena.llm.assistants.BaseAssistant.BaseAssistant"
    agent_id: str = ""
    
def verify_health(base_url):
  print("\n--> Validate the Web App is Alive\n")

  rep = requests.get(base_url + "/health").content.decode()
  print(f"\n@@@> {rep}")
  assert "Alive" in rep


def perform_general_knowledge_query_legacy(base_url):
  print("\n--> Validate Basic Query to LLM\n")
  data='{ "callWithVectorStore": false, "callWithDecisionService": false, "locale": "en",\
    "query": "can you give me some information about langchain",\
    "type": "chat",\
    "modelParameters": { \
      "modelName": "gpt-3.5-turbo-0125",\
      "modelClass": "agent_openai",\
      "prompt_ref": "default_prompt",\
      "temperature": 0,\
      "top_k": 1,\
      "top_p": 1\
    },\
    "chat_history": ""\
  }'
  rep = requests.post(base_url + "/c/generic_chat", data=data, headers = {"Content-Type": "application/json"}).content.decode()
  print(f"\n@@@> {rep}")
  

def validate_access_to_data_mgr():
  print("\n--> Call to get a user to validate data management works\n")

  rep = requests.get("http://localhost:8080/repository/clients/search/Smith").content.decode()
  print(f"\n@@@> {rep}")
  assert "Sonya" in rep

def upload_pdf_insurance_doc(base_url):
  print("\n--> Upload pdf document to vector store\n")
  f = open("../scenarios/ibu-claims-complaint-rules.pdf", "rb")
  files = {'myFile' :  f }
  rep = requests.post(base_url + "/a/documents?name=ibu-claims-complaint-rules&description=The%20rules%20about%20claim%20complaint%20management&type=pdf", files=files).content.decode()
  print(f"\n@@@> {rep}")
 
def validate_access_to_ibu_prompt(base_url):
  print("\n--> Get IBU default prompt\n")
  rep = requests.get(base_url + "/a/prompts/openai_insurance_with_tool").content.decode()
  print(f"\n@@@> {rep}")
  assert "customer service representative" in rep
  
  
def validate_ibu_assistant(base_url):
  print("\n--> Get IBU assistant entity\n")
  resp = requests.get(base_url + "/a/assistants/ibu_assistant")
  a_str= resp.content.decode()
  print(f"\n@@@> {a_str}")
  ae = OwlAssistantEntity.model_validate_json(json_data=a_str)
  print(f"\n@@@> {ae}")
  #print(obj["agent_id"])
  return ae
  

def validate_ibu_agent(base_url,agent_id):
  print("\n--> Get IBU agent entity\n")
  rep = requests.get(base_url + "/a/agents/"+agent_id).content.decode()
  print(f"\n@@@> {rep}")
  return rep

def validate_ibu_tools(base_url, tool_id):
  print("\n--> Get IBU tool entity\n")
  rep = requests.get(base_url + "/a/tools/"+tool_id).content.decode()
  print(f"\n@@@> {rep}")
  return rep


def get_client_using_LLM(base_url, client_id):
  print("\n--> Get client description using tool and llm\n")
  pass

if __name__ == "__main__":
  print("################ Non Regression Tests ##############")
  verify_health(IBU_BASE_URL)
  perform_general_knowledge_query_legacy(IBU_BASE_URL)
  validate_access_to_data_mgr()
  validate_access_to_ibu_prompt(IBU_BASE_URL)
  ae=validate_ibu_assistant(IBU_BASE_URL)
  validate_ibu_agent(IBU_BASE_URL,ae.agent_id)
  validate_ibu_tools(IBU_BASE_URL,"ibu_claim_by_id")






