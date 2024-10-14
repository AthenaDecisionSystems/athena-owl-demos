from ibu.itg.decisions.call_api import Connection
from ibu.itg.decisions.decision_center_extraction import DecisionCenterExtract

base_url = 'http://localhost:9060/decisioncenter-api/v1'
username = 'odmAdmin'
password = 'odmAdmin'
verbose = True
decision_service_name = 'ds-insurance-pc-claims-nba'
path = f'json/{decision_service_name}.json'

connection = Connection(base_url=base_url, username=username, password=password, verbose=verbose)

decision_center_extract = DecisionCenterExtract.create(decision_service_name, connection)
decision_center_extract.save_to_file(path)
