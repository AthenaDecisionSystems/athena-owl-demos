curl -X 'POST' \
  'http://localhost:8000/api/v1/c/generic_chat' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "callWithVectorStore": false,
  "callWithDecisionService": true,
  "local": "en",
  "query": "David Martin is not happy with the settlement of his claim with id number 1. He thinks the amount reimbursed is far too low. He is threatening to leave to the competition.",
  "type": "chat",
  "reset": false,
  "modelParameters": {
    "modelName": "gpt-3.5-turbo-0125",
    "modelClass": "agent_openai",
    "prompt_ref": "openai_insurance_with_tool",
    "temperature": 0,
    "top_k": 1,
    "top_p": 1
  },
  "chat_history": []
}' 