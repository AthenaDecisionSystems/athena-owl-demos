import yaml,sys,os
import unittest
module_path = "./src"
sys.path.append(os.path.abspath(module_path))
os.environ["CONFIG_FILE"] = "./tests/ut/config/config.yaml"

from athena.llm.prompts.prompt_mgr import get_prompt_manager, OwlPromptEntity
from athena.routers.prompts import get_prompt_using_key_and_locale

class TestPrompts(unittest.TestCase):
    
    def test_get_prompt_at_api_level(self):
        thePrompt=get_prompt_using_key_and_locale("openai_insurance_with_tool","en")
        assert thePrompt
        assert "customer service representative" in thePrompt
        
    
    def test_build_en_prompt_from_prompt_entity(self):
        print("\n\n --- test_build_prompt_instance_from_prompt_entity")
        p_mgr=get_prompt_manager()
        prompt = p_mgr.build_prompt("openai_insurance_with_tool","en")
        print(type(prompt))
        print(prompt)
    
    def test_build_fr_prompt_from_prompt_entity(self):
        print("\n\n --- test_build_prompt_instance_from_prompt_entity")
        p_mgr=get_prompt_manager()
        prompt = p_mgr.build_prompt("openai_insurance_with_tool","fr")
        print(type(prompt))
        print(prompt) 
    
    def test_build_es_prompt_from_prompt_entity(self):
        print("\n\n --- test_build_prompt_instance_from_prompt_entity")
        p_mgr=get_prompt_manager()
        prompt = p_mgr.build_prompt("openai_insurance_with_tool","es")
        print(type(prompt))
        print(prompt) 



if __name__ == '__main__':
    unittest.main()