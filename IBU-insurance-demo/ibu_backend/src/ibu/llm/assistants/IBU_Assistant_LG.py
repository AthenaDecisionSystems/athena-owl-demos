"""
Copyright 2024 Athena Decision Systems
@author Jerome Boyer
"""
from typing_extensions import TypedDict
from typing import Annotated, Literal, Any, Optional
import json,logging
from typing import Optional
from athena.app_settings import get_config
from athena.llm.assistants.assistant_mgr import OwlAssistant
from athena.llm.agents.agent_mgr import get_agent_manager, OwlAgentEntity, OwlAgentInterface
from athena.itg.store.content_mgr import get_content_mgr
 
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage, HumanMessage, ToolMessage
from langchain_core.runnables.config import RunnableConfig
from langgraph.pregel.types import StateSnapshot
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.sqlite import SqliteSaver

import langchain

LOGGER = logging.getLogger(__name__)

if get_config().logging_level == "DEBUG":
    langchain.debug=True
    
"""
An assistance to support the contact center agents from IBU insurance for the complaint management process
"""

"""
The graph needs to do a query classification and routing to assess if the query is for complaint or
for gathering information. Once in the complaint branch, the LLM should be able to identify the need
for tool calling and then let one of the Tool node performing the function execution.
Use memory to keep state of the conversation
"""  
class AgentState(TypedDict):
    """
    Keep messages as chat history
    """
    messages: Annotated[list[AnyMessage], add_messages]

class BasicToolNode:
    """A node that runs the tools requested in the last AIMessage."""
    def __init__(self, tools: list) -> None:
        # list of tools of type langchain basetool
        self.tools_by_name = {tool.name: tool for tool in tools}
        LOGGER.debug(f"\n@@@> tools in node: {self.tools_by_name}")

    def __call__(self, inputs: dict):
        # Perform the tool calling if the last message has tool calls list.
        if messages := inputs.get("messages", []):
            last_message = messages[-1]
        else:
            raise ValueError("No message found in input")
        outputs = []   # keep outputs of all the tool calls
        for tool_call in last_message.tool_calls:
            tool_result = self.tools_by_name[tool_call["name"]].invoke(
                tool_call["args"]
            )
            outputs.append(
                ToolMessage(
                    content=json.dumps(tool_result),
                    name=tool_call["name"],
                    tool_call_id=tool_call["id"],
                )
            )
        return {"messages": outputs}

def get_or_build_classifier_model() -> OwlAgentInterface | None:
    # This method is temporary - need to get assistant supporting multiple agents
    
    mgr = get_agent_manager()
    oae: Optional[OwlAgentEntity] = mgr.get_agent_by_id("ibu_classify_query_agent")
    if oae is None:
        raise ValueError("ibu_classify_query_agent agent not found")
    return mgr.build_agent(oae.agent_id,"en")
 
def define_information_q_model() ->OwlAgentInterface | None:
    # This method is temporary - need to get assistant supporting multiple agents
    
    mgr = get_agent_manager()
    oae: Optional[OwlAgentEntity] = mgr.get_agent_by_id("openai_tool_chain")
    if oae is None:
        raise ValueError("openai_tool_chain agent not found")
    return mgr.build_agent(oae.agent_id,"en")


     
class IBUInsuranceAssistant(OwlAssistant):
    
    def __init__(self,agent,assistantID):
        super().__init__(assistantID)
        self.memory = SqliteSaver.from_conn_string(":memory:")
        self.classifier_model: Optional[OwlAgentInterface] = get_or_build_classifier_model()
        self.information_q_model: Optional[OwlAgentInterface] = define_information_q_model()
        self.model = agent.get_model()
        self.prompt = agent.get_prompt()
        self.rag_retriever = get_content_mgr().get_retriever()
        
        tools = agent.get_tools() + self.information_q_model.get_tools()
        tool_node=BasicToolNode(tools) 
        graph = StateGraph(AgentState)
        graph.add_node("classify", self.process_classify_query)
        graph.set_entry_point("classify")
        graph.set_finish_point("classify")
        """
        graph.add_node("information", self.process_information_query)
        graph.add_node("llm", self.call_llm)
        graph.add_node("tools", tool_node)
        
        graph.add_conditional_edges(
            "llm",
            self.route_tools,
            { 
             "tools": "tools", 
             END: END}
        )
        graph.add_conditional_edges(
            "classify",
            self.route_tools,
            {"COMPLAINT": "llm", END: END}
        )
        graph.add_edge("tools", "llm")

        """
        self.graph = graph.compile(checkpointer=self.memory)


    def process_classify_query(self, state: AgentState):
        messages = state['messages']
        print(messages)
        #messages= [convert_message_to_dict(m) for m in messages]
        LOGGER.debug(f"\n@@@> {messages}")
        message = self.classifier_model.invoke(messages)
        return {'messages': [message]}
    
    def retrieve(self, state):
        print("---RETRIEVE---")
        question = state["question"]
        documents = self.rag_retriever.invoke(question)
        return {"documents": documents, "question": question}

    def process_information_query(self, state: AgentState):
        messages = state['messages']
        #messages= [convert_message_to_dict(m) for m in messages]
        LOGGER.debug(f"\n@@@> {messages}")
        message = self.information_q_model.invoke(messages)
        return {'messages': [message]}
    
    def call_llm(self, state: AgentState):  
        messages = state['messages']
        #messages= [convert_message_to_dict(m) for m in messages]
        LOGGER.debug(f"\n@@@> {messages}")
        message = self.model.invoke(messages)
        return {'messages': [message]}
    
   
    def route_tools(self,
        state: AgentState,
    ) -> Literal["tools", END]:
        """Use in the conditional_edge to route to the ToolNode if the last message
        has tool calls. Otherwise, route to the end."""
        if isinstance(state, list):
            ai_message = state[-1]
        elif messages := state.get("messages", []):
            ai_message = messages[-1]
        else:
            raise ValueError(f"No messages found in input state to tool_edge: {state}")
        LOGGER.debug(f"\n@@@> {ai_message}")
        if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
            return "tools"
        return END
    
    def invoke(self, request, thread_id: Optional[str], **kwargs) -> dict[str, Any] | Any:
        self.config: RunnableConfig = {"configurable": {"thread_id": thread_id}}
        messages=[HumanMessage(content=request["input"])]
        resp= self.graph.invoke(messages, self.config)
        msg=resp["messages"][-1].content
        return msg
    
    def get_state(self) -> StateSnapshot:
        return self.graph.get_state(self.config)

    