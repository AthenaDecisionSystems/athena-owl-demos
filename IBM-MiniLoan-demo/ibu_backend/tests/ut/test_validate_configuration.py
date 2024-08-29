"""
Read the assistant config for all assistant and try to instantiate all of them to validate each individual config
"""
import unittest
import os
import sys
from dotenv import load_dotenv
load_dotenv()

os.environ["CONFIG_FILE"] = "./tests/ut/config/config.yaml"
module_path = "./src"
sys.path.append(os.path.abspath(module_path))
from athena.llm.agents.agent_mgr import get_agent_manager

class TestValidateConfiguration(unittest.TestCase):
    
    def test_load_all_agents(self):
        mgr = get_agent_manager()
        for agent_entity in mgr.get_agents():
            print(f"Create instance for {agent_entity}")
            agent_runner = mgr.build_agent_runner(agent_entity,"en")
            assert agent_runner

if __name__ == '__main__':
    unittest.main()