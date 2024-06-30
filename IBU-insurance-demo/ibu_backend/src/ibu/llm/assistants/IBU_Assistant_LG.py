"""
Copyright 2024 Athena Decision Systems
@author Jerome Boyer
"""
from typing_extensions import TypedDict
from athena.app_settings import get_config
from athena.llm.assistants.assistant_mgr import OwlAssistant
from typing import Annotated, Literal, Any
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage, HumanMessage, ToolMessage
from langgraph.pregel.types import StateSnapshot
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.sqlite import SqliteSaver
import json,logging
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

    
class IBUInsuranceAssistant(OwlAssistant):
    
    def __init__(self,agent,assistantID):
        super().__init__(assistantID)
        self.memory = SqliteSaver.from_conn_string(":memory:")
        self.model = agent.get_model()
        self.prompt = agent.get_prompt()
        tool_node=BasicToolNode(agent.get_tools())
        graph = StateGraph(AgentState)
        graph.add_node("classify", self.classify_query)
        graph.add_node("llm", self.call_llm)
        graph.add_node("tools", tool_node)
        graph.add_conditional_edges(
            "llm",
            self.route_tools,
            {"tools": "tools", END: END}
        )
        graph.add_edge("classify", "llm")
        graph.add_edge("tools", "llm")
        graph.set_entry_point("classify")
        self.graph = graph.compile(checkpointer=self.memory)


    def classify_query(self, state: AgentState):
        messages = state['messages']
        #messages= [convert_message_to_dict(m) for m in messages]
        LOGGER.debug(f"\n@@@> {messages}")
        message = self.classifier_model.invoke(messages)
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
    
    def get_state(self) -> StateSnapshot:
        return self.graph.get_state(self.config)

    