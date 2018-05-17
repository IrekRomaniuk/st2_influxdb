from infsensor import InfMaxSensor

class PanSensor(InfMaxSensor):
    """
    TESTING
    curl -i -XPOST 'http://1.1.1.1:8086/write?db=firewalls' --data-binary 'cpu,firewall=TST-PAN,site=TST value=90'    
    """
    def __init__(self, sensor_service, config, poll_interval):             
        super(PanSensor, self).__init__(sensor_service=sensor_service, config=config, poll_interval=poll_interval, 
                                        value='cpu_load', measurement='cpu_load', 
                                        tags =['site','firewall','coreid','dsp'], skip_zero=True) # ,'coreid','dsp'
    