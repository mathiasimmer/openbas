from smap.services.zonecontroller import ZoneController

class AvgSensorFollowMaster(ZoneController):
    def setup(self, opts):
        ZoneController.setup(self, opts)
        # we want to publish the heat/cool setpoints
        self.add_timeseries('/temp_heat','F',data_type='double')
        self.add_timeseries('/temp_cool','F',data_type='double')
        # we want to write a special averaging function to handle the temperature sensors, so
        # we use add_callback to run it automatically when new sensor data comes in
        self.add_callback('temp_sensor', self.avg_temp, opts.get('subscribe/temp_sensor'))

    def step(self):
        # adjust heat/cool setpoints by the difference between the thermostat temperature and the
        # average room setpoint
        new_diff = self.points['thermostat_temp'] - self.points['avg_temp']
        self.points['temp_heat'] += new_diff
        self.points['temp_cool'] += new_diff
        self.add('/temp_heat', float(self.points['temp_heat']))
        self.add('/temp_cool', float(self.points['temp_cool']))

    def avg_temp(self, point, uuids, data):
        # averages the readings
        self.points['avg_temp'] = sum(map(lambda x: x[-1][1], data)) / float(len(data))
