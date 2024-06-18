
from typing_extensions import TypedDict
from athena.app_settings import get_config
from athena.llm.assistants.assistant_mgr import OwlAssistant
from athena.routers.dto_models import ConversationControl, ResponseControl
from typing import Annotated, Literal, Any
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, ToolMessage
from langgraph.pregel.types import StateSnapshot
from langgraph.checkpoint.sqlite import SqliteSaver
import json,logging
import langchain

LOGGER = logging.getLogger(__name__)

if get_config().logging_level == "DEBUG":
    langchain.debug=True
"""
An assistance to support CSM from IBU insurance for the claim processing process
"""

class AgentState(TypedDict):
    """
    Keep messages as chat history
    """
    messages: Annotated[list[AnyMessage], add_messages]

class BasicToolNode:
    """A node that runs the tools requested in the last AIMessage."""
    def __init__(self, tools: list) -> None:
        self.tools_by_name = {tool.name: tool for tool in tools}
        LOGGER.debug(f"\n@@@> tools in node: {self.tools_by_name}")

    def __call__(self, inputs: dict):
        if messages := inputs.get("messages", []):
            message = messages[-1]
        else:
            raise ValueError("No message found in input")
        outputs = []
        for tool_call in message.tool_calls:
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
    
"""
A two node graph to integrate with tools and LLM
"""    
class IBUAssistant(OwlAssistant):
    
    def __init__(self,agent):
        self.memory = SqliteSaver.from_conn_string(":memory:")
        self.model = agent.get_runnable()
        tool_node=BasicToolNode(agent.get_tools())
        graph = StateGraph(AgentState)
        graph.add_node("llm", self.call_llm)
        graph.add_node("tools", tool_node)
        graph.add_conditional_edges(
            "llm",
            self.route_tools,
             {"tools": "tools", END: END}
        )
        graph.add_edge("tools", "llm")
        graph.set_entry_point("llm")
        self.graph = graph.compile(checkpointer=self.memory)
    
    def call_llm(self, state: AgentState):
        messages = state['messages']
        print(messages)
        message = self.model.invoke(messages)
        return {'messages': [message]}
    
   
    def route_tools(self, state: AgentState) -> Literal["tools", END]:
        result = state['messages'][-1]
        return len(result.tool_calls) > 0
    
    def get_state(self) -> StateSnapshot:
        return self.graph.get_state(self.config)
    

    def invoke(self, query: str, thread_id: str) -> dict[str, Any] | Any:
        self.config = {"configurable": {"thread_id": thread_id}}
        m=HumanMessage(content=query)
        resp= self.graph.invoke({"messages":[m]}, self.config)
        return resp
    
    def send_conversation(self, controller: ConversationControl) -> ResponseControl | Any:
        graph_rep= self.invoke(controller.query, controller.thread_id)
        resp = ResponseControl()
        resp.message=graph_rep["messages"][-1].content
        resp.chat_history=[ m.json() for m in graph_rep["messages"]]
        resp.assistant_id=controller.assistant_id
        resp.thread_id=controller.thread_id
        resp.user_id = controller.user_id
        return resp
    