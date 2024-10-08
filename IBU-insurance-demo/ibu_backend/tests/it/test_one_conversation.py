
import unittest

import requests
import json
import sys
sys.path.append('./src')

from athena.routers.dto_models import ConversationControl, ResponseControl

IBU_BASE_URL="http://localhost:8002/api/v1"


class TestAppApi(unittest.TestCase):


    def get_response_control(self, rep) -> str:
        print(f"\n@@@> {rep}")
        rep_dict= json.loads(rep)
        repControl = ResponseControl.model_validate(rep_dict)
        return repControl
    
    def test_validate_history(self):
        """
        Send a message, get the history and then reinject the history
        """
        print("\n--> test_validate_history\n")
        cc = ConversationControl()
        cc.agent_id="ibu_agent"
        cc.user_id="remote_test"
        cc.thread_id="T1"
        cc.chat_history=[]
        cc.query="hello"

        data=cc.model_dump_json()
        rep = requests.post(IBU_BASE_URL + "/c/generic_chat", data=data, headers = {"Content-Type": "application/json"}, timeout = 10).content.decode()
        repControl= self.get_response_control(rep)
        assert len(repControl.chat_history) == 2
        print(repControl)
        cc.chat_history=repControl.chat_history
        data=cc.model_dump_json()
        rep = requests.post(IBU_BASE_URL + "/c/generic_chat", data=data, headers = {"Content-Type": "application/json"}, timeout = 10).content.decode()
        repControl= self.get_response_control(rep)
        print(repControl)
        assert len(repControl.chat_history) == 4
        
        

if __name__ == '__main__':
    unittest.main()