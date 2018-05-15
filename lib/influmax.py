def InfluxmaxSensor():
    self._logger.debug('rep dispatching trigger...')        
    result = self._client.query(self._query)
    points = list(result.get_points(measurement=MEASUREMENT)) #, tags=tags
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
        i = ":".join([string_point[tag] for tag in TAGS])
        self._logger.debug('point {} of value {}'.format(i,int(string_point[VALUE])))
        if i not in minimum:
            minimum[i] = DUMMY
        if int(string_point[VALUE]) < minimum[i]:
            self._logger.debug('SKIP_ZERO {} and value {} is below {}'.format(SKIP_ZERO, int(string_point[VALUE]), minimum[i]))
            if SKIP_ZERO and (int(string_point[VALUE]) == 0) :                    
                payload['zeros_pts'] += 1
            else:                      
                minimum[i] = int(string_point[VALUE])
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