from infsensor import InfMaxSensor

class ChpSensor(InfMaxSensor):
    """
    TESTING
    curl -i -XPOST 'http://1.1.1.1:8086/write?db=firewalls' --data-binary 'cpu,firewall=TST-CHP,site=TST value=90'    
    """
    def __init__(self, sensor_service, config, poll_interval):             
        super(ChpSensor, self).__init__(sensor_service=sensor_service, config=config, poll_interval=poll_interval, 
                                        value='value', measurement='cpu', 
                                        tags =['site','firewall', 'id', 'proc'], skip_zero=True)
    