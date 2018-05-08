from st2reactor.sensor.base import PollingSensor
from influxdb import InfluxDBClient

VALUE='*'
MEASUREMENT='cpu'

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
    """
    def __init__(self, sensor_service, config=None, poll_interval=None):
        super(RepvpnSensor, self).__init__(sensor_service=sensor_service, 
                                          config=config,
                                          poll_interval=poll_interval)
        self._logger = self.sensor_service.get_logger(name=self.__class__.__name__)        
        
    def setup(self):
        self._db = self._config['db'] # or None
        self._user = self._config['username']
        self._pass = self._config['password']
        self._base_url, self._port = self._config['base_url'].split(":") 
        # print(self._base_url, self._port, self._user, self._pass, self._db)    
        self._client = InfluxDBClient(self._base_url, self._port, self._user, self._pass, self._db)
        self._query="select {0} from {1} WHERE time > now() - {2}s;".format(VALUE, MEASUREMENT, self._poll_interval) 
        self._max=int(self._config['max'])   
        self.sensor_service.set_value('influxdb.max', self._max)    

    def poll(self):        
        self._logger.debug('rep dispatching trigger...')
        # count = self.sensor_service.get_value('influxdb.count') or 0
        result = self._client.query(self._query)
        points = list(result.get_points(measurement=MEASUREMENT)) #, tags=tags
        max = {}
        max_all = 0
        alert_saved = self.sensor_service.get_value('influxdb.alert') or 0
        payload = {}
        for point in points:
            string_point=dict([(str(k), str(v)) for k, v in point.items()])
            i = string_point['site'] + ":" + string_point['firewall'] + ":" + string_point['id'] + ":" + string_point['proc']
            if i not in max:
                max[i] = 0
            if int(string_point['value']) > max[i]:
                # print(string_point)               
                max[i] = int(string_point['value'])
                payload[i]=int(max[i])
                #self.sensor_service.set_value('influxdb.alert', True)
                if int(string_point['value']) > max_all:
                    max_all = int(string_point['value'])
                    payload['max_all'] = int(string_point['value'])                    

        payload['num_pts'] = len(points)
        payload['max'] = int(self.sensor_service.get_value('influxdb.max')) or 98
        self.sensor_service.dispatch(trigger='influxdb.rep_cpu', payload=payload)
        # self.sensor_service.set_value('influxdb.count', payload['count'])      

    def cleanup(self):
        pass

    # Methods required for programmable sensors.
    def add_trigger(self, trigger):
        pass

    def update_trigger(self, trigger):
        pass

    def remove_trigger(self, trigger):
        pass