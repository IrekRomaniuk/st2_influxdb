from influxdb import InfluxDBClient

from st2actions.runners.pythonrunner import Action
"""
python test/influx.py
"""
CPUMAX=20
WINDOW=60
result_list=[]
class query(Action):
       
    def run(self, value, measurement): #, tags
        _db = self.config['db']
        _user = self.config['username']
        _pass = self.config['password']
        _base_url, _port = self.config['base_url'].split(":") 
        # print(_db,_user, _pass, _base_url, _port)    
        client = InfluxDBClient(_base_url, _port, _user, _pass, _db)
        query="select {0} from {1} WHERE time > now() - {2}s;".format(value, measurement, WINDOW)
        result = client.query(query)
        points = list(result.get_points(measurement=measurement)) #, tags=tags
        for point in points:
            string_point=dict([(str(k), str(v)) for k, v in point.items()])
            if int(string_point['value'])>CPUMAX:
                # print(string_point)
                result_list.append(string_point)
                # print result_list
        return (result_list)    
