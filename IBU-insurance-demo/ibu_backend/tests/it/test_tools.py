import unittest

import sys,os
os.environ["CONFIG_FILE"] = "./tests/it/config/config.yaml"
sys.path.append('./src')
from ibu.llm.tools.client_tools import get_claim_status_by_user_name


class TestTools(unittest.TestCase):
    
    def test_claim_status(self):
        client = get_claim_status_by_user_name("Sonya", "Smith")
        assert client
        print(client)

if __name__ == '__main__':
    unittest.main()