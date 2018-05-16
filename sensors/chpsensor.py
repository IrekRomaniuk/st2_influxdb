from repsensor import RepvpnSensor

class ChpSensor(RepvpnSensor):
    """
    TESTING
    curl -i -XPOST 'http://1.1.1.1:8086/write?db=firewalls' --data-binary 'cpu,firewall=TST,site=TST value=90'    
    """
    def __init__(self, value, measurement, tags, skip_zero):             
        super(ChpSensor, self).__init__(value = 'value', measurement = 'cpu', tags = ['site','firewall', 'id', 'proc'], skip_zero = True)
        