import logging

import bme680


class Sensor:
    def __init__(self):
        self.sensor = self.configure_sensor()
        logging.debug('Initial reading:')
        for name in dir(self.sensor.data):
            value = getattr(self.sensor.data, name)

            if not name.startswith('_'):
                logging.debug('{}: {}'.format(name, value))
        self.sensor.set_gas_heater_temperature(320)
        self.sensor.set_gas_heater_duration(150)
        self.sensor.select_gas_heater_profile(0)

    def configure_sensor(self):
        try:
            sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
        except IOError:
            sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)
        sensor.set_humidity_oversample(bme680.OS_2X)
        sensor.set_pressure_oversample(bme680.OS_4X)
        sensor.set_temperature_oversample(bme680.OS_8X)
        sensor.set_filter(bme680.FILTER_SIZE_3)
        sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)
        return sensor

    async def get_sensor_data(self):
        data = {}
        if self.sensor.get_sensor_data():
            data.update({
                "temperature": self.sensor.data.temperature,
                "pressure": self.sensor.data.pressure,
                "humidity": self.sensor.data.humidity,
            })
            if self.sensor.data.heat_stable:
                data.update({
                    "gas_resistance": self.sensor.data.gas_resistance
                })

        return data

