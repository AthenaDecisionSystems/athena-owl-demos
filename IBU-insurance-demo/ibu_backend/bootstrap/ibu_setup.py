import sys, os


import make_insurance_glossary
import make_insurance_prompts

"""
Build the different elements related to a specific demonstration
"""

print("\t###################")
print("\   Define insurance glossary")
make_insurance_glossary.define_glossary("../config/glossary.json")
print("\   Define insurance LLM prompts")
make_insurance_prompts.define_insurance_prompts("../config/prompts.json")
print("\t###################")