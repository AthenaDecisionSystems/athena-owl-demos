"""
Copyright 2024 Athena Decision Systems
@author Jerome Boyer
"""
import json
import logging
from typing import Annotated, Any, Optional, Literal, List
from typing_extensions import TypedDict
import langchain
from langchain_core.prompts import BasePromptTemplate
from langchain_core.messages import AnyMessage, ToolMessage, HumanMessage, AIMessage
from langchain_core.runnables.config import RunnableConfig
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langgraph.pregel.types import StateSnapshot
from langgraph.checkpoint.memory import MemorySaver

from athena.llm.agents.agent_mgr import OwlAgentDefaultRunner, OwlAgent, get_agent_manager
from ibu.app_settings import get_config
from athena.itg.store.content_mgr import get_content_mgr
from athena.llm.tools.tool_mgr import OwlToolEntity
from athena.routers.dto_models import ConversationControl, ResponseControl
from langgraph.prebuilt import ToolNode, tools_condition

"""
An assistance to support the contact center agents from IBU insurance for the complaint management process.

The graph needs to do a query classification and routing to assess if the query is for complaint management or
for gathering information. Once in the complaint branch, the LLM should be able to identify the need
for tool calling and then let one of the Tool node performing the function execution.

Use memory to keep state of the conversation
"""  

LOGGER = logging.getLogger(__name__)
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

if get_config().logging_level == "DEBUG":
    langchain.debug=True

class AgentState(TypedDict):
    """
    Keep messages as chat history: message can be human, ai or tool messages.
    question asked by user, and documents retrieved from vector store
    """
    messages: Annotated[list[AnyMessage], add_messages]
    documents: List[str]
    input: str

def define_classifier_model():
    return get_agent_manager().build_agent_runner("ibu_classify_query_agent","en")

def define_ibu_tool_rag_agent_limited():
    return get_agent_manager().build_agent_runner("ibu_tool_rag_agent_limited","en")

def define_ibu_tool_rag_agent():
    return get_agent_manager().build_agent_runner("ibu_tool_rag_ds_agent","en")

    
class IBUInsuranceAgent(OwlAgentDefaultRunner):

    def __init__(self, agentEntity: OwlAgent, prompt: Optional[BasePromptTemplate], tool_instances: Optional[list[OwlToolEntity]]):
        self.agent_id = agentEntity.agent_id
        self.classifier_model= define_classifier_model()
        self.information_q_model = define_ibu_tool_rag_agent_limited() # TODO could comes for subagent list
        self.complaint_model = define_ibu_tool_rag_agent()
        #tool_node=BasicToolNode(tool_instances)
        self.use_vector_store = False
        self.build_the_graph()
       

    def build_the_graph(self):
        graph_builder = StateGraph(AgentState)
        graph_builder.set_conditional_entry_point(
            self.process_classify_query,
            {
                "information": "gather_information",
                "complaint": "process_complaint",
            },
        )
        graph_builder.add_node("gather_information", self.process_information_query)
        graph_builder.add_node("process_complaint", self.process_complaint)
        graph_builder.add_edge("gather_information", END)
        graph_builder.add_edge("process_complaint", END)
        self.graph = graph_builder.compile(checkpointer=MemorySaver())

    def process_information_query(self, state):
        question = state["input"]
        messages = state['messages']
        #uestion= messages[-1]
        if self.use_vector_store:
            state["documents"] = self.rag_retriever.invoke(question)
        else:
            state["documents"] = []
        documents = state["documents"]

        message = self.information_q_model.invoke({"input": [question], 
                                                   "context": documents,    
                                                   "chat_history": messages},
                                                    self.config["configurable"]["thread_id"]) # dict
        return {'messages': [AIMessage(content=message["output"])], "input" : message["input"]}
    
    def process_classify_query(self, state: AgentState):
        messages = state['messages']
        question = state["input"]
        #messages= [convert_message_to_dict(m) for m in messages]
        LOGGER.debug(f"\n@@@> {messages}")
        message = self.classifier_model.invoke({"input": [question], 
                                                "chat_history": messages}, 
                                                self.config["configurable"]["thread_id"])
        if "information" in message.lower():
            LOGGER.debug("---ROUTE QUESTION TO INFORMATION---")
            return "information"
        elif "complaint"  in message.lower():
            LOGGER.debug("---ROUTE QUESTION TO Complaint---")
            return "complaint"
        # TODO Decide what to do if none of this 
    
    def process_complaint(self, state):  
        messages = state['messages']
        question = state["input"]
        if self.use_vector_store:
            state["documents"] = self.rag_retriever.invoke(question)
        else:
            state["documents"] = []
        documents = state["documents"]
        message = self.complaint_model.invoke({"input": question,
                                               "context": documents, 
                                                "chat_history": messages},
                                                self.config["configurable"]["thread_id"])
        return {'messages': [AIMessage(content=message["output"])]}
    
    # ==================== overrides =============================
    def invoke(self, request, thread_id: Optional[str], **kwargs) -> dict[str, Any] | Any:
        if kwargs["vector_store"]:
            self.use_vector_store = True
        self.config: RunnableConfig = {"configurable": {"thread_id": thread_id}}
        m=HumanMessage(content=request["input"])
        resp= self.graph.invoke({"messages": [m], "input": m}, self.config)
        msg=resp["messages"][-1].content
        return msg
    
    def get_state(self) -> StateSnapshot:
        return self.graph.get_state(self.config)
    
    def send_conversation(self, controller: ConversationControl) -> ResponseControl | Any:
         # overwrite the default. 
        request = { "input": controller.query }
        agent_resp= self.invoke(request, controller.thread_id, vector_store = controller.callWithVectorStore)   # AIMessage
        resp = self.build_response(controller,agent_resp)
        return resp