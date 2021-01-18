import logging

from aioprometheus import pusher, Gauge, Registry


TEMPERATURE = Gauge("temperature", "Temperature")
PRESSURE = Gauge("pressure", "Pressure")
HUMIDITY = Gauge("humidity", "Humidity")
GAS_RESISTANCE = Gauge("gas_resistance", "Gas resistance")


class PushGatewayMetrics:
    def __init__(self, store):
        self.store = store
        self.pusher = pusher.Pusher("weather", "http://127.0.0.1:9091")
        self.registry = Registry()
        self.registry.register(TEMPERATURE)
        self.registry.register(PRESSURE)
        self.registry.register(HUMIDITY)
        self.registry.register(GAS_RESISTANCE)

    async def push_weather_data(self):
        weather = self.store.stored_data.get('weather_sensor', {})
        TEMPERATURE.set({}, weather.get("temperature"))
        PRESSURE.set({}, weather.get("pressure"))
        HUMIDITY.set({}, weather.get("humidity"))
        GAS_RESISTANCE.set({}, weather.get("gas_resistance"))
        try:
            await self.pusher.replace(self.registry)
        except OSError:
            logging.error("Failed to push metrics to pushgateway")
