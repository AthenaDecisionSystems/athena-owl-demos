"""
Copyright 2024 Athena Decision Systems
@author Jerome Boyer
"""
from typing_extensions import TypedDict
from typing import Annotated, Literal, Any, Optional, List
from langchain_core.pydantic_v1 import BaseModel, Field
import json,logging

from athena.app_settings import get_config
from athena.llm.assistants.assistant_mgr import OwlAssistant
from athena.llm.agents.agent_mgr import get_agent_manager, OwlAgentEntity, OwlAgentInterface
from athena.routers.dto_models import ConversationControl, ResponseControl
from athena.itg.store.content_mgr import get_content_mgr
 
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage, HumanMessage, AIMessage, ToolMessage
from langchain_core.runnables.config import RunnableConfig
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.schema import Document
from langgraph.pregel.types import StateSnapshot
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import StateGraph, START, END

import langchain

LOGGER = logging.getLogger(__name__)
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

if get_config().logging_level == "DEBUG":
    langchain.debug=True
  
"""
An assistance to support the contact center agents from IBU insurance for the complaint management process.

The graph needs to do a query classification and routing to assess if the query is for complaint management or
for gathering information. Once in the complaint branch, the LLM should be able to identify the need
for tool calling and then let one of the Tool node performing the function execution.

Use memory to keep state of the conversation
"""  

class AgentState(TypedDict):
    """
    Keep messages as chat history: message can be human, ai or tool messages.
    question asked by user, and documents retrieved from vector store
    """
    messages: Annotated[list[AnyMessage], add_messages]
    documents: List[str]
    question: str

    

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
        for tool_call in set(last_message.tool_calls):  # use a set to void calling same tool multiple time
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

def web_search(state):
    print("---WEB SEARCH---")
    question = state["question"]
    web_search_tool = TavilySearchResults(k=3)
    docs = web_search_tool.invoke({"query": question})
    web_results = "\n".join([d["content"] for d in docs])
    web_results = Document(page_content=web_results)
    return {"documents": web_results, "question": question}
     
class IBUInsuranceAssistant(OwlAssistant):
    
    def __init__(self, assistantID, agents):
        super().__init__(assistantID, agents)
        self.memory = SqliteSaver.from_conn_string(":memory:")
        # As of now the order of declaration of the agent is important, so 0 match the classification agent
        self.classifier_model: Optional[OwlAgentInterface] = agents[0]
        self.information_q_model: Optional[OwlAgentInterface] = agents[1]
        self.complaint_model = agents[2].get_runnable()
        self.use_vector_store = False
        self.prompt = agents[2].get_prompt()
        # the following may change when retriever will be tool
        self.rag_retriever = get_content_mgr().get_retriever()
        tool_node_1=BasicToolNode(self.information_q_model.get_tools())
        tool_node_2=BasicToolNode(agents[2].get_tools())
        
        # ================= DEFINE GRAPH ====================
        graph = StateGraph(AgentState)
        graph.add_node("gather_information", self.process_information_query)
        graph.add_node("process_complaint", self.process_complaint)
        graph.add_node("activate_tools_for_info", tool_node_1)
        graph.add_node("activate_tools_for_complaint", tool_node_2)
        graph.set_conditional_entry_point(
            self.process_classify_query,
            {
                "information": "gather_information",
                "complaint": "process_complaint",
            },
        )
        
        graph.add_conditional_edges(
            "gather_information",
            self.route_tools,
            { 
             "tools": "activate_tools_for_info", 
             END: END}
        )
        graph.add_edge("activate_tools_for_info", "gather_information")
        graph.add_conditional_edges(
            "process_complaint",
            self.route_tools,
            { 
             "tools": "activate_tools_for_complaint", 
             END: END}
        )
        graph.add_edge("activate_tools_for_complaint", "process_complaint")

        self.graph = graph.compile(checkpointer=self.memory)


    def process_classify_query(self, state: AgentState):
        messages = state['messages']
        question = state["question"]
        #messages= [convert_message_to_dict(m) for m in messages]
        LOGGER.debug(f"\n@@@> {messages}")
        message = self.classifier_model.invoke({"question": question})
        if message.next_task == "information":
            print("---ROUTE QUESTION TO INFORMATION---")
            return "information"
        elif message.next_task == "complaint":
            print("---ROUTE QUESTION TO Complaint---")
            return "complaint"


    def process_information_query(self, state):
        question = state["question"]
        if self.use_vector_store:
            state["documents"] = self.rag_retriever.invoke(question)
        documents = state["documents"]

        message = self.information_q_model.invoke({"question": question, "context": documents}) # dict
        return {'messages': [AIMessage(content=message["output"])], "question" : message["question"]}
    
    def process_complaint(self, state):  
        messages = state['messages']
        question = state["question"]
        if self.use_vector_store:
            state["documents"] = self.rag_retriever.invoke(question)
        else:
            state["documents"] = []
        documents = state["documents"]
        LOGGER.debug(f"\n@@@> {messages}")
        message = self.complaint_model.invoke({"question": question, "context": documents})
        return {'messages': [AIMessage(content=message["output"])]}
    
   
    def route_tools(self,
        state: AgentState,
    ) -> Literal["tools", END]:
        """Use in the conditional_edge to route to the ToolNode if the last message
        has tool calls. Otherwise, route to the end."""
        if messages := state.get("messages", []):
            ai_message = messages[-1]
            LOGGER.debug(f"\n@@@> {ai_message}")
        else:
            raise ValueError(f"No messages found in input state to tool_edge: {state}")
        
        if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
            return "tools"
        return END
    
    def invoke(self, request, thread_id: Optional[str], **kwargs) -> dict[str, Any] | Any:
        if kwargs["vector_store"]:
            self.use_vector_store = True
        self.config: RunnableConfig = {"configurable": {"thread_id": thread_id}}

        resp= self.graph.invoke(request, self.config)
        msg=resp["messages"][-1].content
        return msg
    
    def get_state(self) -> StateSnapshot:
        return self.graph.get_state(self.config)

    
    def send_conversation(self, controller: ConversationControl) -> ResponseControl | Any:
         # overwrite the default. 
        request = { "question": controller.query }
        agent_resp= self.invoke(request, controller.thread_id, vector_store = controller.callWithVectorStore)   # AIMessage
        resp = self._build_response(controller)
        resp.message=agent_resp
        return resp