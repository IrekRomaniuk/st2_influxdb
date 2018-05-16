from repsensor import RepvpnSensor

class ChpSensor(RepvpnSensor):
    """
    TESTING
    curl -i -XPOST 'http://1.1.1.1:8086/write?db=firewalls' --data-binary 'cpu,firewall=TST,site=TST value=90'    
    """
    def __init__(self, sensor_service, config, poll_interval, value, measurement, tags, skip_zero):             
        super(ChpSensor, self).__init__(sensor_service=sensor_service, config=config,poll_interval=poll_interval,
                                        value = 'value', measurement = 'cpu', tags = ['site','firewall', 'id', 'proc'], skip_zero = True)
    