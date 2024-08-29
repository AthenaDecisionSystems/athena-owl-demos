"""
a bunch of calls to the backend servers to validate the major functions
"""
from pydantic import BaseModel
from typing import Optional
import requests


IBU_BASE_URL="http://localhost:8000/api/v1"
PROMPT_REFERENCE="ibu_loan_prompt"
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

def verify_health(base_url):
  print("\n--> Validate the Web App is Alive\n")

  rep = requests.get(base_url + "/health").content.decode()
  print(f"\n@@@> {rep}")
  assert "Alive" in rep
  

def validate_access_to_ibu_prompt(base_url):
  print("\n--> Get IBU default prompt\n")
  rep = requests.get(base_url + f"/a/prompts/{PROMPT_REFERENCE}/en").content.decode()
  print(f"\n@@@> {rep}")
  assert "bank" in rep
  
  
def validate_ibu_agent(base_url):
  print("\n--> Get IBU Loan agent entity\n")
  resp = requests.get(base_url + f"/a/agents/{AGENT_REF}")
  a_str= resp.content.decode()
  print(f"\n@@@> {a_str}")
  ae = OwlAgent.model_validate_json(json_data=a_str)
  print(f"\n@@@> {ae}")
  #print(obj["agent_id"])
  return ae
  


def validate_ibu_tools(base_url, tool_id):
  print("\n--> Get IBU loan tool entity\n")
  rep = requests.get(base_url + "/a/tools/"+tool_id).content.decode()
  print(f"\n@@@> {rep}")
  return rep

def validate_get_credit_score(base_url, fn: str, ln: str):
  print("\n--> Get information about one of the client\n")
  question = "What is the credit score of Robert Smith using IBU loan database?"
  print("\n the question: {question}")
  data='{ "locale": "en",\
    "query": "' + question+ '",\
    "agent_id": "ibu_agent", \
    "thread_id" : "1", \
    "user_id" : "a_test_user"\
  }'
  rep = requests.post(base_url + "/c/generic_chat", data=data, headers = {"Content-Type": "application/json"}).content.decode()
  print(f"\n@@@> {rep}")
  return rep

def validate_approve_a_loan(base_url, fn: str, ln: str):
  print(f"\n--> Assess a loan for {fn} {ln}\n")
  question= f"\"One of our client {fn} {ln} wants a loan for $1,000,000 for 180 months with a yearly repayment of $60,000  do we approve it?\""
  data='{ "locale": "en",\
    "query": ' + question +',\
    "agent_id": "ibu_agent", \
    "thread_id" : "1", \
    "user_id" : "a_test_user"\
  }'
  rep = requests.post(base_url + "/c/generic_chat", data=data, headers = {"Content-Type": "application/json"}).content.decode()
  print(f"\n@@@> {rep}")
  return rep

def validate_approve_a__good_loan(base_url, fn: str, ln: str):
  print(f"\n--> Assess a loan for {fn} {ln}\n")
  question=f"\"My client {fn} {ln} wants to get a $200,000 loan for a period of 120 months for his house enhancement with a yearly repayment of $40,000 , do you think it is possible?\""
  data='{ "locale": "en",\
    "query": ' + question +',\
    "agent_id": "ibu_agent", \
    "thread_id" : "1", \
    "user_id" : "a_test_user"\
  }'
  rep = requests.post(base_url + "/c/generic_chat", data=data, headers = {"Content-Type": "application/json"}).content.decode()
  print(f"\n@@@> {rep}")
  return rep



if __name__ == "__main__":
  print("################ Non Regression Tests ##############") 
  verify_health(IBU_BASE_URL)
  validate_access_to_ibu_prompt(IBU_BASE_URL)
  ae=validate_ibu_agent(IBU_BASE_URL)
  validate_ibu_tools(IBU_BASE_URL,"ibu_client_by_name")
  validate_get_credit_score(IBU_BASE_URL,"Robert", "Smith")
  validate_approve_a_loan(IBU_BASE_URL,"Robert", "Smith")
  validate_approve_a__good_loan(IBU_BASE_URL,"Jean", "Martin")






