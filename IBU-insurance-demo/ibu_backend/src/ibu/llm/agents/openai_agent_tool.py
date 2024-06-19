"""
Copyright 2024 Athena Decision Systems
@author Jerome Boyer
"""
from langchain_openai import ChatOpenAI
from langchain.agents import create_tool_calling_agent
from langchain.agents import AgentExecutor
from langchain_core.runnables import Runnable
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from athena.llm.base_owl_agent import BaseOwlAgent
from athena.routers.dto_models import ConversationControl
from athena.llm.tools.tool_mgr import OwlToolEntity
from athena.llm.prompts.prompt_mgr import get_prompt_manager
from athena.app_settings import get_config
from ibu.itg.tool_manager import get_tools_to_use
import langchain

if get_config().logging_level == "DEBUG":
    langchain.debug=True

class OpenAIAgent(BaseOwlAgent):

    def __init__(self, modelName, system_prompt, temperature, top_p, tool_entities: list[OwlToolEntity]):
        self.system_prompt = system_prompt
        self.model = ChatOpenAI(model=modelName, temperature= temperature / 50)
        
        
    def get_model(self, modelName, stream, callbacks):
        return ChatOpenAI(model=modelName , temperature=0)  
    
    def get_agent(self, model, prompt, tools ) -> Runnable:
        return create_tool_calling_agent(model, tools, prompt)

    def build_agent_executor(self,controller:ConversationControl,stream = False, callbacks = None):
        prompt= self.assess_what_prompt_to_use(controller)
        tools = get_tools_to_use(controller)
        if controller.modelParameters is not None and controller.modelParameters.modelName != "":
            self.model = self.get_model( controller.modelParameters.modelName,stream,callbacks)
       
        self.model.bind_tools(tools)
        theAgent = self.get_agent(self.model, prompt, tools)
        return AgentExecutor(agent=theAgent, tools=tools, verbose=True)

    

    def assess_what_prompt_to_use(self,controller:ConversationControl):
        """
        Looking at the query and the fact to use decision service or not and vector store, select the matching prompt
        """
        if controller.modelParameters is not None and controller.modelParameters.prompt_ref != "":
            self.system_prompt = get_prompt_manager().get_prompt(controller.modelParameters.prompt_ref,controller.locale)
        # conversationControl.type does not seem necessary
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            MessagesPlaceholder(variable_name="context", optional=True),
            MessagesPlaceholder(variable_name="chat_history", optional=True),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad", optional=True),
        ])

        return  prompt