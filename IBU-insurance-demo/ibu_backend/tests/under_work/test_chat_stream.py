import requests
import sys
from pydantic import BaseModel
sys.path.append('./src')
from athena.routers.dto_models import ConversationControl

class ChatMessage(BaseModel):
    content: str

query= "what is langsmith?"
convControl = ConversationControl.model_validate({
                    "callWithVectorStore": False, 
                    "callWithDecisionService": False,  
                    "type": "chat", 
                    "query": query
                    }
                )
dt=convControl.model_dump_json()
headers = {"Content-type" : "application/json"}

with requests.post("http://localhost:8000/c/chat",data=dt, headers= headers, stream=True) as r:
    for chunk in r.iter_content(100):
        print(chunk)