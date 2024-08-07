"""
Copyright 2024 Athena Decision Systems
@author Jerome Boyer
"""
from langchain_openai import ChatOpenAI
from langchain.agents import create_openai_tools_agent
from langchain.agents import AgentExecutor
from athena.llm.base_owl_agent import BaseOwlAgent
from athena.routers.dto_models import ConversationControl
from athena.app_settings import get_config
from ibu.itg.tool_manager import get_tools_to_use
import langchain

if get_config().logging_level == "DEBUG":
    langchain.debug=True

class OpenAIClient(BaseOwlAgent):


    def get_model(self, model_name, stream, callbacks):
        return ChatOpenAI(model=model_name, temperature=0)  
    
    def get_agent(self, model, prompt, tools ):
        return create_openai_tools_agent(model, tools, prompt)
    


    def build_agent_executor(self,controller:ConversationControl,stream = False, callbacks = None):
        prompt= self.assess_what_prompt_to_use(controller)
        tools = get_tools_to_use(controller)
        if controller.modelParameters is not None and controller.modelParameters.modelName != "":
            model = self.get_model( controller.modelParameters.modelName,stream,callbacks)
        else:
            model = self.get_model(get_config().owl_agent_llm_model,stream,callbacks)
        model.bind_tools(tools)
        agent = self.get_agent(model, prompt, tools)
        return AgentExecutor(agent=agent, tools=tools, verbose=True)

    

    