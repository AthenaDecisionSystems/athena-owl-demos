from athena.llm.tools.tool_mgr import OwlToolEntity

from athena.llm.agents.agent_mgr import OwlAgentInterface, OwlAgentEntity

from typing import Literal
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.agents import  AgentExecutor
from langchain_core.prompts import BasePromptTemplate

class RouteQuery(BaseModel):
    """Route a user query to the most relevant task."""
    next_task: Literal["complaint", "information"] = Field(
        ...,
        description="Given a user question choose to route it to information or a complaint task.",
    )
    
class IBUClassifyQueryAgent(OwlAgentInterface):
    
    def __init__(self, agentEntity: OwlAgentEntity, prompt: BasePromptTemplate, tool_entities: list[OwlToolEntity]):
        self.model = ChatOpenAI(model=agentEntity.modelName, temperature= agentEntity.temperature / 50)
        # as we build a special prompt needs to get the template for the system prompt. it looks like a hack
        self.system_prompt = prompt.dict()["messages"][0]['prompt']['template']
        #
        structured_llm_router = self.model.with_structured_output(RouteQuery)
        self.route_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", self.system_prompt),
                ("human", "{question}"),
            ]
        )
        self.router_agent = self.route_prompt | structured_llm_router
    
    def get_prompt(self):
        return self.route_prompt
    
    def get_model(self):
        return self.model
    
    def invoke(self, query, **kwargs) -> str:
        return self.router_agent.invoke(query)
    
    def get_tools(self):
        return []