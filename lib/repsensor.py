from st2reactor.sensor.base import PollingSensor
from influxdb import InfluxDBClient
import ast, requests

# VALUE= 'value'
# MEASUREMENT='cpu'
# TAGS = ['site','firewall', 'id', 'proc'] # 'site','firewall', 'id', 'proc'
# SKIP_ZERO = True # skip zero values
class RepvpnSensor(PollingSensor):
    """
    * self.sensor_service
        - provides utilities like
            get_logger() for writing to logs.
            dispatch() for dispatching triggers into the system.
    * self._config
        - contains configuration that was specified as
          config.yaml in the pack.
    * self._poll_interval
        - indicates the interval between two successive poll() calls.
    Testing:
    curl -i -XPOST 'http://1.1.1.1:8086/write?db=firewalls' --data-binary 'cpu,firewall=TST,site=TST value=90'    
    """
    def __init__(self, sensor_service, config=none, poll_interval=None, value='', measurement='', tags=[], skip_zero=True): # sensor_service, config=None, poll_interval=None, 
        super(RepvpnSensor, self).__init__(sensor_service=sensor_service, 
                                          config=config,
                                          poll_interval=poll_interval)
        self._logger = self.sensor_service.get_logger(name=self.__class__.__name__)
          
        self.value = value # 'value'
        self.measurement = measurement # 'cpu'
        self.tags = tags # ['site','firewall', 'id', 'proc'] # 'site','firewall', 'id', 'proc'
        self.skip_zero = skip_zero # True # skip zero values

        
    def setup(self):
        self._db = self._config['db'] # or None
        self._user = self._config['username']
        self._pass = self._config['password']
        self._base_url, self._port = self._config['base_url'].split(":")           
        self._client = InfluxDBClient(self._base_url, self._port, self._user, self._pass, self._db)
        self._query="select {0} from {1} WHERE time > now() - {2}s;".format('*', self.measurement, self._poll_interval) 
        self._max=int(self._config['max'])   
        self.sensor_service.set_value('influxdb.max', self._max)    

    def poll(self):        
        self._logger.debug('rep dispatching trigger...')   
        DUMMY=999     
        result = self._client.query(self._query)
        points = list(result.get_points(measurement=self.measurement)) #, tags=tags
        minimum = {}
        alert_saved = ast.literal_eval(self.sensor_service.get_value('influxdb.alert')) or False
        self._logger.debug('alert_saved {} type {}'.format(alert_saved, type(alert_saved)))
        payload = {}
        payload['alert_saved']=alert_saved #testing only
        alert = False  
        payload['zeros_pts'] = 0
        payload['below_pts'] = 0
        current = 0
        alerted = ''
        for point in points:
            string_point=dict([(str(k), str(v)) for k, v in point.items()])            
            i = ":".join([string_point[tag] for tag in self.tags])
            self._logger.debug('point {} of value {}'.format(i,int(string_point[self.value])))
            if i not in minimum:
                minimum[i] = DUMMY
            if int(string_point[self.value]) < minimum[i]:
                self._logger.debug('self.skip_zero {} and value {} is below {}'.format(self.skip_zero, int(string_point[self.value]), minimum[i]))
                if self.skip_zero and (int(string_point[self.value]) == 0) :                    
                    payload['zeros_pts'] += 1
                else:                      
                    minimum[i] = int(string_point[self.value])
                    payload[i]=int(minimum[i])  
                    payload['below_pts'] += 1                                  
        
        minimum = {k:v for k,v in minimum.items() if v != DUMMY}
        # if minimum:

        key_max = max(minimum.keys(), key=(lambda k: minimum[k]))
        cpu_max = minimum[key_max]
        payload['alert'] = False
        self._logger.debug('minimum {} '.format(minimum))
        if cpu_max < self._max:
            self._logger.debug('cpu_max {} < self._max {}'.format(cpu_max, self._max))
            alert = False            
            if alert_saved != alert:
                self._logger.debug('alert_saved {} != alert {}'.format(alert_saved, alert))
                # self._logger.debug('alert_saved {}, alert {}'.format(type(alert_saved), type(alert)))
                payload['alert'] = True
                self.sensor_service.set_value('influxdb.alert', False)
                payload['current'] = cpu_max
                payload['alerted'] = ""
        else:
            for i, cpu in minimum.iteritems():
                    if cpu > self._max:
                        current = cpu
                        alerted = i
                        break 
            self._logger.debug('cpu_max {} >= self._max {} for {}'.format(cpu_max, self._max, alerted))
            alert = True                      
            if alert_saved != alert:
                payload['alert'] = True
                self.sensor_service.set_value('influxdb.alert', True)                                   
                payload['current'] = cpu
                payload['alerted'] = i                  

        payload['num_pts'] = len(points)
        payload['max'] = int(self.sensor_service.get_value('influxdb.max')) or 98
        requests.get("https://hchk.io/f48b4815-cb37-417b-ae93-fafb6faec53f")
        self.sensor_service.dispatch(trigger='influxdb.rep_cpu', payload=payload)     

    def cleanup(self):
        pass

    # Methods required for programmable sensors.
    def add_trigger(self, trigger):
        pass

    def update_trigger(self, trigger):
        pass

    def remove_trigger(self, trigger):
        pass