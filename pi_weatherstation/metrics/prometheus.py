import logging

from aioprometheus import pusher, Gauge, Registry, Service


TEMPERATURE = Gauge("temperature", "Temperature")
PRESSURE = Gauge("pressure", "Pressure")
HUMIDITY = Gauge("humidity", "Humidity")
GAS_RESISTANCE = Gauge("gas_resistance", "Gas resistance")

PROMETHEUS_SERVER = Service()


class PrometheusMetrics:
    def __init__(self, store):
        self.store = store
        PROMETHEUS_SERVER.register(TEMPERATURE)
        PROMETHEUS_SERVER.register(PRESSURE)
        PROMETHEUS_SERVER.register(HUMIDITY)
        PROMETHEUS_SERVER.register(GAS_RESISTANCE)

    async def start_prometheus_server(self):
        await PROMETHEUS_SERVER.start(addr="0.0.0.0", port=9191)
        logging.info((f"Serving prometheus metrics on: {PROMETHEUS_SERVER.metrics_url}"))

    async def push_weather_data(self):
        weather = self.store.stored_data.get('weather_sensor')
        if not weather:
            logging.debug("Weather data unavailable")
            return
        TEMPERATURE.set({}, weather.get("temperature"))
        PRESSURE.set({}, weather.get("pressure"))
        HUMIDITY.set({}, weather.get("humidity"))
        GAS_RESISTANCE.set({}, weather.get("gas_resistance"))
