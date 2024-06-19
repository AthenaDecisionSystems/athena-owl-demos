"""
Copyright 2024 Athena Decision Systems
@author Jerome Boyer
"""
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import  AgentExecutor
from langchain.agents import create_tool_calling_agent
from langchain_core.output_parsers import StrOutputParser
from athena.llm.tools.tool_mgr import OwlToolEntity
from athena.llm.base_owl_agent import BaseOwlAgent
from ibu.llm.tools import claim_tools
from ibu.llm.tools import client_tools

class IBUAgent(BaseOwlAgent):
    
    def __init__(self, modelName, system_prompt, temperature, top_p, tool_entities: list[OwlToolEntity]):
        self.model = ChatOpenAI(model=modelName, temperature= temperature / 50)
        self.tools = self.build_tool_instances(tool_entities)
        self.system_prompt = system_prompt
        self.prompt =  ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="context", optional=True),
            MessagesPlaceholder(variable_name="chat_history", optional=True),
            ("human", "{messages}"),
            MessagesPlaceholder(variable_name="agent_scratchpad", optional=True),
        ])

    
    def get_prompt(self):
        return self.prompt
    
    def get_model(self):
        return self.model
    
    def get_agent(self, model, prompt, tools ):
        """
        A Runnable sequence representing an agent. It takes as input all the same input
        variables as the prompt passed in does. It returns as output either an
        AgentAction or AgentFinish.
        """
        return create_tool_calling_agent(model, tools, prompt)
    
    def get_runnable(self):
        #llm_with_tool= self.model.bind_tools(self.tools)
        #agent=create_openai_tools_agent(self.model, self.tools, self.prompt)
        #return AgentExecutor(agent=agent, tools=self.tools, verbose=True)
        #return self.prompt | llm_with_tool | StrOutputParser()
        self.model.bind_tools(self.tools)
        theAgent = self.get_agent(self.model, self.prompt, self.tools)
        return AgentExecutor(agent=theAgent, tools=self.tools, verbose=True)
    
    def get_tools(self):
        return self.tools
        
    def build_tool_instances(self, tool_entities: list[OwlToolEntity]):
        tool_list=[]
        for tool_entity in tool_entities:
            if tool_entity.tool_id == "ibu_claim_by_id":
                tool_list.append( claim_tools.define_tool(tool_entity.tool_name, tool_entity.tool_description, tool_entity.tool_fct_name))
            elif "client" in tool_entity.tool_id:
                tool_list.append(client_tools.define_tool(tool_entity.tool_name, tool_entity.tool_description, tool_entity.tool_fct_name))
            elif  tool_entity.tool_id == "ibu_best_action":
                tool_list.append(claim_tools.define_tool(tool_entity.tool_name, tool_entity.tool_description, tool_entity.tool_fct_name))
            else:
                raise Exception(f"{tool_entity.tool_id}: Not yet implemented")
        return tool_list