import json

import requests
from requests.auth import HTTPBasicAuth


class Connection:
    def __init__(self, base_url: str, username: str, password: str, verbose: bool = False):
        """
        Initialize the connection class with the API URL, username, and password.
        Uses HTTP Basic Authentication for authorization.
        """
        self.base_url = base_url
        self.auth = HTTPBasicAuth(username, password)  # Initialize auth with self.username and self.password
        self.verbose = verbose

    def call_request(self, method: str, endpoint: str, **kwargs) -> dict:
        """
        Make a request to the specified API endpoint and forwarding the arguments to the original requests.request function
        """
        url = f"{self.base_url}/{endpoint}"
        response = requests.request(method, url, auth=self.auth, **kwargs)

        if response.status_code == 200:
            json_response = response.json()
            if self.verbose:
                print(endpoint, json.dumps(json_response, indent=4))
            return json_response
        else:
            response.raise_for_status()
