import requests
import sys, json
sys.path.append('./src')

from ibu.itg.ds.ComplaintHandling_generated_model import *

data_mgr_url="http://localhost:8080/repository"

resp=requests.get(data_mgr_url + "/claims/1")
print(resp.text)
claim = Claim(**json.loads(resp.text))
#claim=resp.text
print(claim)


