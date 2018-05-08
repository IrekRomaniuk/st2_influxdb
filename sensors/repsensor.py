from st2reactor.sensor.base import PollingSensor
from influxdb import InfluxDBClient

# CPUMAX=20
WINDOW=60
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
        self._query="select {0} from {1} WHERE time > now() - {2}s;".format(VALUE, MEASUREMENT, WINDOW)

    def poll(self):        
        self._logger.debug('rep dispatching trigger...')
        # count = self.sensor_service.get_value('influxdb.count') or 0
        result = self._client.query(self._query)
        points = list(result.get_points(measurement=MEASUREMENT)) #, tags=tags
        max = {}
        for point in points:
            string_point=dict([(str(k), str(v)) for k, v in point.items()])
            # i = string_point['site'] + ":" + string_point['firewall'] + ":" + string_point['id'] + ":" + string_point['proc']
            i = 'firewall'
            if i not in max:
                max[i] = 0
            if int(string_point['value']) > max[i]:
                # print(string_point)               
                max[i] = int(string_point['value'])
                payload = {
                    'site': string_point['site'], 
                    'firewall': string_point['firewall'], 
                    'id': string_point['id'],
                    'proc': string_point['proc'],
                    'value': string_point['value']
                }
        
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