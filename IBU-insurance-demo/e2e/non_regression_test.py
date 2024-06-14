"""
a bunch of calls to the backend servers to validate the major functions
"""

import requests

URL="http://localhost:8000/api/v1"
print("################ Non Regression Tests ##############")
print("--> Validate the Web App is Alive")

rep = requests.get(URL + "/health").content.decode()
print(rep)
assert "Alive" in rep

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
  "chat_history": []\
}'
rep = requests.post(URL + "/c/generic_qa", data=data, headers = {"Content-Type": "application/json"}).content.decode()
print(rep)

print("\n--> Call to get a user to validate data management works\n")

rep = requests.get("http://localhost:8080/repository/clients/search/Smith").content.decode()
print(rep)
assert "Sonya" in rep

print("\n--> Upload pdf document to vector store\n")
f = open("../scenarios/ibu-claims-complaint-rules.pdf", "rb")
files = {'myFile' :  f }
rep = requests.post(URL + "/a/documents?name=ibu-claims-complaint-rules&description=The%20rules%20about%20claim%20complaint%20management&type=pdf", files=files).content.decode()
print(rep)