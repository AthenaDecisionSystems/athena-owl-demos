curl -X 'POST' \
  'http://localhost:8000/api/v1/c/generic_qa' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "callWithVectorStore": false,
  "callWithDecisionService": true,
  "local": "en",
  "query": "David Martin is not happy with the settlement of his claim with id number 1. He thinks the amount reimbursed is far too low. He is threatening to leave to the competition.",
  "type": "qa",
  "chat_history": []
}' 