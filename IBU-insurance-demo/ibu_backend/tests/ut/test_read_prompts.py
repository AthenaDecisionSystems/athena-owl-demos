import yaml,sys,os
import unittest
module_path = "./src"
sys.path.append(os.path.abspath(module_path))
os.environ["CONFIG_FILE"] = "./tests/ut/config/config.yaml"

from athena.llm.prompts.prompt_mgr import get_prompt_manager
from athena.routers.prompts import get_prompt_using_key_and_locale

class TestPrompts(unittest.TestCase):
    
    def test_get_prompt_at_api_level(self):
        thePrompt=get_prompt_using_key_and_locale("openai_insurance_with_tool","en")
        assert thePrompt
        assert "UnsatisfiedWithQualityOfCustomerService" in thePrompt
        
    def test_validate_classification_lama_prompt(self):
        p_mgr=get_prompt_manager()
        prompt = p_mgr.build_prompt("classify_query__llama_prompt","en")
        assert prompt
        assert len(prompt.optional_variables) > 0
        assert len(prompt.messages) > 0
        assert prompt.messages[0].prompt.template
        assert "begin_of_text" in prompt.messages[0].prompt.template

    def test_validate_classification_prompt(self):
        p_mgr=get_prompt_manager()
        prompt = p_mgr.build_prompt("classify_query_prompt","en")
        assert prompt
        assert len(prompt.optional_variables) > 0
        assert len(prompt.messages) > 0
        assert prompt.messages[0].prompt.template
        assert "extracting intent from user questions" in prompt.messages[0].prompt.template


    def test_validate_classification_prompt(self):
        p_mgr=get_prompt_manager()
        prompt = p_mgr.build_prompt("classify_query__llama_prompt","en")
        assert prompt
        assert len(prompt.optional_variables) > 0
        assert len(prompt.messages) > 0
        assert prompt.messages[0].prompt.template
        assert "begin_of_text" in prompt.messages[0].prompt.template

    def test_build_en_prompt_from_prompt_entity(self):
        print("\n\n --- test_build_en_prompt_from_prompt_entity")
        p_mgr=get_prompt_manager()
        prompt = p_mgr.build_prompt("ibu_insurance_mistral_prompt","en")
        assert prompt
        assert len(prompt.optional_variables) > 0
        assert len(prompt.messages) > 0
        assert prompt.messages[0].prompt.template
        print(prompt)
    





if __name__ == '__main__':
    unittest.main()