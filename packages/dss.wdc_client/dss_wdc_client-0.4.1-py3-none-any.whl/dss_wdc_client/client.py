import pandas as pd
import requests
import logging
import os


class WDCClient: 
    
    @staticmethod
    def fromEnv():
        """Create a WDCClient from the 'Environment'
        
        Uses the environment variables 'WDC_HOST' and 'WDC_TOKEN' from the current
        environment. Thus you can make use of modules such as python-dotenv
        or other variants more easily.
        
        Remember: Using passwords or tokens in source code is dangerous!
        """
        _host = os.getenv('WDC_HOST')
        _token = os.getenv('WDC_TOKEN')
        
        client = WDCClient(host = _host, token = _token)
        
        return client

    def __init__(self, host: str, token = None):
        self.logger = logging.getLogger(__name__)
        self.host = host 
        self.token = token
        
        if self.host == None:
            raise Exception("Could not create WDCClient with host = None")
        
        self.session = requests.Session()
        if self.token != None: 
            self.session.headers.update({'token': self.token})

        
    def loadAsDataFrame(self, endpoint: str) -> pd.DataFrame: 
        json = self.loadAsJson(endpoint);
        
        return pd.json_normalize(json)
        
        
    def loadAsJson(self, endpoint: str) -> []: 
        res = []
        url = self.host + "/" + endpoint
        
        while url != None: 
            response = self.session.get(url)
            self.logger.debug("headers: %s", response.headers)
    
            json = response.json()
            
            res.extend(json["content"])
            
            # gehts weiter?
            if 'links' in json and 'next' in json['links']:
                url = json['links']['next']
                self.logger.debug("nextLink %s", next)
            else: 
                url = None
        
        return res

    def __str__(self) -> str:
        return "[host=" + str(self.host) + ", token=" + str(self.token) + "}"