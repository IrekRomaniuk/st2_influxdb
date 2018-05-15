from st2reactor.sensor.base import PollingSensor
from influxdb import InfluxDBClient
import ast, requests
from common_lib import influmax

VALUE= 'value'
DUMMY=999
MEASUREMENT='cpu'
TAGS = ['site','firewall', 'id', 'proc'] # 'site','firewall', 'id', 'proc'
SKIP_ZERO = True # skip zero values
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
        self._client = InfluxDBClient(self._base_url, self._port, self._user, self._pass, self._db)
        self._query="select {0} from {1} WHERE time > now() - {2}s;".format('*', MEASUREMENT, self._poll_interval) 
        self._max=int(self._config['max'])   
        self.sensor_service.set_value('influxdb.max', self._max)    

    def poll(self):        
        self._logger.debug('rep dispatching trigger...')        
        influmax()
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