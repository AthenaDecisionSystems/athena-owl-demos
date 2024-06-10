## Testing with pytest
- start ODM Execution Server  
- run `pytest`

## Generating Python pydantic data models from ODM decision service OpenAPI spec
- pip install datamodel-code-generator

- datamodel-codegen  --input data/openapi/ComplaintHandlingNextBestActionDecisionService.yaml --output genmodel2.py
