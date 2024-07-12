
from athena.app_settings import get_config, AppSettings
from athena.llm.agents.agent_mgr import OwlAgentInterface, OwlAgentEntity

from langchain_core.output_parsers import StrOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
#from langchain.agents.format_scratchpad.openai_tools import format_to_openai_tool_messages
#from langchain.agents.output_parsers.tools import ToolsAgentOutputParser
from langchain_core.prompts import BasePromptTemplate

import logging
from typing import Optional, Any


logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')
LOGGER = logging.getLogger(__name__)

class IbuToolRagAgent(OwlAgentInterface):
    tools = None
    
    def __init__(self, agentEntity: OwlAgentEntity, prompt: BasePromptTemplate, tool_instances: Optional[list[Any]]):
        LOGGER.debug("Initialing base chain IbuToolRagAgent")
        # do not use the created prompt template only the text as system prompt
        self.prompt = ChatPromptTemplate.from_messages([
                        ("system",  prompt.dict()["messages"][0]['prompt']['template']),
                        ("human", "{question}"),
                        MessagesPlaceholder(variable_name="agent_scratchpad", optional=True),
                    ])
        self.model=self._instantiate_model(agentEntity.modelName, agentEntity.modelClassName, agentEntity.temperature)
        if tool_instances:
            self.tools = tool_instances
            agent = create_tool_calling_agent(self.model, self.tools, self.prompt)
            self.llm = AgentExecutor(agent= agent, tools=self.tools, verbose=True)
            
        else:
            self.llm = {"question": lambda x: x["question"]}  | self.prompt | self.model | StrOutputParser()
            
       
    def get_runnable(self):
        #return   self.prompt |  self.model.bind(self.tools) | StrOutputParser()
        return  self.llm
    

    