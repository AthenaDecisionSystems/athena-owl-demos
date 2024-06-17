"""
a bunch of calls to the backend servers to validate the major functions
"""

import requests
IBU_BASE_URL="http://localhost:8000/api/v1"

def verify_health(base_url):
  print("--> Validate the Web App is Alive")

  rep = requests.get(base_url + "/health").content.decode()
  print(rep)
  assert "Alive" in rep


def perform_general_knowledge_query(base_url):
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
  print(rep)
  

def validate_access_to_data_mgr():
  print("\n--> Call to get a user to validate data management works\n")

  rep = requests.get("http://localhost:8080/repository/clients/search/Smith").content.decode()
  print(rep)
  assert "Sonya" in rep

def upload_pdf_insurance_doc(base_url):
  print("\n--> Upload pdf document to vector store\n")
  f = open("../scenarios/ibu-claims-complaint-rules.pdf", "rb")
  files = {'myFile' :  f }
  rep = requests.post(base_url + "/a/documents?name=ibu-claims-complaint-rules&description=The%20rules%20about%20claim%20complaint%20management&type=pdf", files=files).content.decode()
  print(rep)
  
if __name__ == "__main__":
  print("################ Non Regression Tests ##############")
  # verify_health(IBU_BASE_URL)
  perform_general_knowledge_query(IBU_BASE_URL)
  # validate_access_to_data_mgr()






