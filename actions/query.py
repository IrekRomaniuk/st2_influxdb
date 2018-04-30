import sys, requests, xmltodict, json, urllib3
from string import Template
from influxdb import InfluxDBClient
import json

from st2actions.runners.pythonrunner import Action
"""
python test/influx.py
"""
CPUMAX=20
WINDOW=600
result_list=[]
class query(Action):
       
    def run(self, , value, measurement, tags):
        _db = self.config['db']
        _user = self.config['username']
        _pass = self.config['password']
        _base_url, _port = self.config['base_url'].split(":") 
        client = InfluxDBClient(_base_url, 8086, _user', _pass, _db)
        query="select {0} from {1} WHERE time > now() - {1}s;".format(value, measurement, WINDOW)
        result = client.query(query)
        points = list(result.get_points(measurement=measurement, tags=tags))
        for point in points:
            string_point=dict([(str(k), str(v)) for k, v in point.items()])
            if int(string_point['value'])>CPUMAX:
            #print(string_point)
            result_list.append(string_point)
        return (result_list)    
