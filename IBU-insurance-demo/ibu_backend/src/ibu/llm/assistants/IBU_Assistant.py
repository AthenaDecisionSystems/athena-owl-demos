"""
Copyright 2024 Athena Decision Systems
@author Jerome Boyer
"""
from athena.llm.assistants.assistant_mgr import OwlAssistant
from athena.routers.dto_models import ConversationControl, ResponseControl
from athena.app_settings import get_config
from athena.routers.dto_models import ConversationControl, ResponseControl
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage

from typing import Any

import json,logging
import langchain

LOGGER = logging.getLogger(__name__)

if get_config().logging_level == "DEBUG":
    langchain.debug=True
    
class IBUAssistant(OwlAssistant):
    
    def __init__(self,agent):
        self.agent = agent
    
    def send_conversation(self, controller: ConversationControl) -> ResponseControl | Any:
        LOGGER.debug(f"In send_conversation legacy {controller}")
        agent_executor =  self.agent.build_agent_executor(controller,False)
        chat_history = controller.chat_history
        resp = ResponseControl()
        agentResponse=agent_executor.invoke({"input": controller.query, "chat_history":chat_history})
        LOGGER.debug(f"---> {agentResponse}")
        resp.chat_history=agentResponse["chat_history"]
        # should we build the history here?
        resp.message=agentResponse["output"]
        LOGGER.debug(resp)
        return resp 
    
