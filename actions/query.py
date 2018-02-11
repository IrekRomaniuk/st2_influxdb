import sys, requests, xmltodict, json, urllib3
from string import Template

from st2actions.runners.pythonrunner import Action
"""
curl -kG ‘https://10.110.111.10:8086/query?pretty=true' — data-urlencode “db=NOAA_water_database” — data-urlencode “q=SELECT * FROM h2o_feet LIMIT 3” -u “phantom:phantom” | jq ‘.’ 
"""
class query(Action):
       
    def run(self, db, user, pass):
        _db = self.config['db']
        _user = self.config['username']
        _pass = self.config['password']
        _base_url = self.config['base_url']
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        url = "https://" + _base_url + "/query?pretty=true"
        try:
            response = requests.post()
        except requests.exceptions.ConnectionError:
            _result['"{}"'.format(firewall)] = "ConnectionError"
            return (False, _result)

        return (True, _result)    
