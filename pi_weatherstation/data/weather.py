import logging


try:
    import pi_weatherstation.data.sensors.bme680 as sensor
except ModuleNotFoundError:
    logging.warning("Problem loading sensor module, using debug sensor")
    import pi_weatherstation.data.sensors.debug as sensor


class Weather:
    def __init__(self, store):
        self.store = store
        self.sensor = sensor.Sensor()

    async def update_weather(self):
        logging.debug("Updating weather data")
        sensor_data = await self.sensor.get_sensor_data()
        if not sensor_data:
            return
        self.store.update({
            "weather_sensor": sensor_data
        })
