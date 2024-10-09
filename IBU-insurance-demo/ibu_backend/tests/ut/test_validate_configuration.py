"""
Read the agent config for all agent and try to instantiate all of them to validate each individual config
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
    
    def test_load_all_agents_and_create_runner_instances(self):
        agent_mgr = get_agent_manager()
        for agent_entity in agent_mgr.get_agents():
            print(f"Create instance for {agent_entity}")
            agent = agent_mgr.build_agent_runner(agent_entity,"en")
            assert agent
            assert agent.agent_id
            print(agent.agent_id)


if __name__ == '__main__':
    unittest.main()