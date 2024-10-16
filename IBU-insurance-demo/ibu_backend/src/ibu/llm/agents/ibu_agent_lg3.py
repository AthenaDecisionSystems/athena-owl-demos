"""
Copyright 2024 Athena Decision Systems
@author Jerome Boyer
"""
import json
import logging
from typing import Annotated, Any, Optional, Literal, List, Union
from typing_extensions import TypedDict
import langchain
from langchain_core.prompts import BasePromptTemplate
from langchain_core.messages import AnyMessage, ToolMessage, HumanMessage, AIMessage
from langchain_core.runnables.config import RunnableConfig

from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langgraph.pregel.types import StateSnapshot
from langgraph.prebuilt import ToolNode, tools_condition

from athena.routers.dto_models import StyledMessage

from athena.llm.agents.agent_mgr import OwlAgentDefaultRunner, OwlAgent, get_agent_manager
from athena.itg.store.content_mgr import get_content_mgr
from athena.llm.tools.tool_mgr import OwlToolEntity
from athena.routers.dto_models import ConversationControl, ResponseControl
from ibu.app_settings import get_config

from ibu.itg.ds.ComplaintHandling_generated_model import Motive
from pydantic import BaseModel
from ibu.itg.decisions.next_best_action_ds_client import callDecisionService
from ibu.llm.tools.client_tools import build_or_get_instantiate_claim_repo


"""
An assistance to support the contact center agents from IBU insurance for the complaint management process.

The graph needs to do a query classification and routing to assess if the query is for complaint management or
for gathering information. Once in the complaint branch, the LLM should be able to identify the need
for tool calling and then let one of the Tool node performing the function execution.

Use memory to keep state of the conversation
"""  


logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')
LOGGER = logging.getLogger(__name__)
if get_config().logging_level == "DEBUG":
    langchain.debug=True
    LOGGER.setLevel(logging.DEBUG)


""" motive
      - UnsatisfiedWithDelay: when the client is not happy with the time taken to process his claim. For instance, when he has not received any response to settle his claim several weeks after the claim was sent.
      - UnsatisfiedWithAppliedCoverages: when the client has received a settlement offer but is not satisfied because the coverages that he thought were applicable have not been applied, either partially (some coverages have not been applied) or totally (no coverage has been applied).
      - UnsatisfiedWithReimbursedAmount: when the client has received a settlement offer but is not satisfied with the proposed reimbursed amount.
      - UnsatisfiedWithQualityOfCustomerService
      """

class ComplaintInfo(BaseModel):
    claim_id: int
    motive: Motive
    intention_to_leave: bool

class AgentState(TypedDict):
    """
    Keep messages as chat history: message can be human, ai or tool messages.
    question asked by user, and documents retrieved from vector store
    """
    messages: Annotated[list[AnyMessage], add_messages]
    documents: List[str]
    complaint_info: Union[None, ComplaintInfo]
    input: str
    path: str

def define_classifier_model():
    #return get_agent_manager().build_agent_runner("ibu_classify_query_agent","en")
    return get_agent_manager().build_agent_runner("ibu_classify_query_watson_agent","en")

def define_information_model():
    return get_agent_manager().build_agent_runner("ibu_information_agent","en")

def define_complaint_agent():
    agent_runner = get_agent_manager().build_agent_runner("ibu_complaint_agent2","en")
    return agent_runner.get_runnable().agent


def define_extract_info_agent():
    agent_runner = get_agent_manager().build_agent_runner("extract_info_to_decide","en")
    return agent_runner.get_runnable().agent

def format_docs(docs):
    list_messages = []  
    for doc in docs:
        list_messages.append(doc.page_content)
    return list_messages


class IBUInsuranceAgent(OwlAgentDefaultRunner):

    def __init__(self, agentEntity: OwlAgent, prompt: Optional[BasePromptTemplate], tool_instances: Optional[list[OwlToolEntity]]):
        self.agent_id = agentEntity.agent_id
        self.classifier_model= define_classifier_model()
        self.information_q_model = define_information_model() # TODO could comes for subagent list
        self.complaint_model = define_complaint_agent()
        self.extract_info_agent = define_extract_info_agent()
        self.tool_node=ToolNode(tool_instances)
        self.use_vector_store = False
        self.use_decision_svc = False
        self.rag_retriever= get_content_mgr().get_retriever()
        self.build_the_graph()
       

    def build_the_graph(self):
        graph_builder = StateGraph(AgentState)
        graph_builder.set_conditional_entry_point(
            self.process_classify_query,
            {
                "information": "gather_information",
                "complaint_with_decision": "extract_info",
                "complaint_with_no_decision": "process_complaint",
                "other": END
            },
        )
        graph_builder.add_node("gather_information", self.process_information_query)
        graph_builder.add_edge("gather_information", END)

        graph_builder.add_node("process_complaint", self.process_complaint)
        graph_builder.add_edge("process_complaint", END)

        graph_builder.add_node("extract_info", self.extract_info)
        graph_builder.add_node("call_decision_service", self.call_decision_service)
        graph_builder.add_edge("extract_info", "call_decision_service")
        graph_builder.add_edge("call_decision_service", END)

        self.checkpointer=MemorySaver()
        self.graph = graph_builder.compile(checkpointer=self.checkpointer)

   
    def process_information_query(self, state):
        question = state["input"].content
        messages = state['messages']
        #uestion= messages[-1]
        if self.use_vector_store and self.rag_retriever:
            state["documents"] = self.rag_retriever.invoke(question)
        else:
            state["documents"] = []
        documents = state["documents"]

        message = self.information_q_model.invoke({"input": [question], 
                                                   "context": format_docs(documents),
                                                   "chat_history": messages},
                                                    self.config["configurable"]["thread_id"]) # dict
        return {'messages': [AIMessage(content=message["output"])]}
    
    def process_classify_query(self, state: AgentState):
        messages = state['messages']
        question = state["input"].content
        #messages= [convert_message_to_dict(m) for m in messages]
        LOGGER.debug(f"\n@@@> {messages}")
        message = self.classifier_model.invoke({"input": [question], 
                                                "chat_history": messages}, 
                                                self.config["configurable"]["thread_id"])
        if "information" in message.lower():
            LOGGER.debug("---ROUTE QUESTION TO INFORMATION---")
            return "information"
        elif "complaint"  in message.lower():
            self.use_decision_svc = True
            if self.use_decision_svc:
                LOGGER.debug("---ROUTE QUESTION TO Complaint handling with decision ---")
                return "complaint_with_decision"
            else:
                LOGGER.debug("---ROUTE QUESTION TO Complaint handling with no decision ---")
                return "complaint_with_no_decision"
        else:
            return "other"

    
    def process_complaint(self, state):  
        messages = state['messages']
        question = state["input"].content
        if self.use_vector_store and self.rag_retriever:
            state["documents"] = self.rag_retriever.invoke(question)
        else:
            state["documents"] = []
        documents = state["documents"]
        messages = self.complaint_model.runnable.invoke({"input": [question],
                                               "context": format_docs(documents),
                                               "chat_history": messages,
                                                "intermediate_steps": [] }
                                               )
        
        return {'messages': messages,'path': 'complaint'}
    
    def extract_info(self, state):  
        LOGGER.warning("--- Extracting information ---")

        messages = state['messages']
        question = state["input"].content
        documents = []
        result = self.extract_info_agent.runnable.invoke({"input": [question],
                                               "context": format_docs(documents),
                                               "chat_history": messages,
                                                "intermediate_steps": [] }
                                               )

        output_elements = result.return_values['output'].split(',')
        motive = output_elements[0]
        intention_to_leave = output_elements[1] == "True"
        claim_id: int = int(output_elements[2])

        complaint_info = ComplaintInfo(claim_id =claim_id, 
                                       motive = motive, 
                                       intention_to_leave = intention_to_leave)
        LOGGER.warning(complaint_info)
        return {
            "complaint_info": complaint_info
        }
    
    def call_decision_service(self, state):  
        LOGGER.info(f"--- Calling the decision service with claim {state['complaint_info'].claim_id} ---")

        config = get_config()
        result = callDecisionService(config, build_or_get_instantiate_claim_repo(), state['complaint_info'].claim_id, state['complaint_info'].motive, state['complaint_info'].intention_to_leave, "en")

        LOGGER.info(result)

        return {
            'messages': "Sonya Smith nous fait chier, elle arrête pas de se plaindre"
        }


    # ==================== overrides =============================
    def invoke(self, request, thread_id: Optional[str], **kwargs) -> dict[str, Any] | Any:
        if kwargs["vector_store"]:
            self.use_vector_store = True
        if kwargs["decision_svc"]:
            self.use_decision_svc = True
        self.config: RunnableConfig = {"configurable": {"thread_id": thread_id}}
        user_input=HumanMessage(content=request)
        resp= self.graph.invoke({"messages": [user_input], "input": user_input}, self.config)
        msg=resp["messages"][-1].content
        return msg
    
    def get_state(self) -> StateSnapshot:
        return self.graph.get_state(self.config)
    
    def send_conversation(self, controller: ConversationControl) -> ResponseControl | Any:
        """
        Override the default as the history is kept in the graph state
        and we need to take into account the tools needed dynamically
        There is no need to process closed questions too
        """ 
        agent_resp= self.invoke(controller.query, 
                                controller.thread_id, 
                                vector_store = controller.callWithVectorStore,
                                decision_svc = controller.callWithDecisionService)   # AIMessage
        resp = self.build_response(controller,agent_resp)
        return resp
    