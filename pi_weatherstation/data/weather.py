import logging


class Weather:
    def __init__(self, store):
        self.temperature = 10
        self.pressure = 200
        self.humidity = 50
        self.gas_resistance = 100
        self.store = store

    async def update_weather(self):
        logging.debug("Updating weather data")
        self.temperature = self.temperature + 1
        self.pressure = self.pressure + 1
        self.humidity = self.humidity + 1
        self.gas_resistance = self.gas_resistance + 1

        self.store.update({
            "weather_sensor": {
                "temperature": self.temperature,
                "pressure": self.pressure,
                "humidity": self.humidity,
                "gas_resistance": self.gas_resistance,
            }
        })
