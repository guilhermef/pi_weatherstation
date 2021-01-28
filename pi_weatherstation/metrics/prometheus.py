import logging

import pi_weatherstation
import pi_weatherstation.config as config

from aioprometheus import Gauge, Service


TEMPERATURE = Gauge("temperature", "Temperature")
PRESSURE = Gauge("pressure", "Pressure")
HUMIDITY = Gauge("humidity", "Humidity")
GAS_RESISTANCE = Gauge("gas_resistance", "Gas resistance")
AIR_QUALITY = Gauge("air_quality", "Air quality")

PROMETHEUS_SERVER = Service()


class PrometheusMetrics:
    def __init__(self, store):
        self.store = store
        PROMETHEUS_SERVER.register(TEMPERATURE)
        PROMETHEUS_SERVER.register(PRESSURE)
        PROMETHEUS_SERVER.register(HUMIDITY)
        PROMETHEUS_SERVER.register(GAS_RESISTANCE)
        PROMETHEUS_SERVER.register(AIR_QUALITY)

    async def start_prometheus_server(self):
        await PROMETHEUS_SERVER.start(
            addr=config.get("metrics_host"),
            port=config.getint("metrics_port"),
        )
        logging.info(
            (f"Serving prometheus metrics on: {PROMETHEUS_SERVER.metrics_url}")
        )

    async def push_weather_data(self):
        weather = self.store.stored_data.get("weather_sensor")
        if not weather:
            logging.debug("Weather data unavailable")
            return
        labels = {
            "pi_weatherstation_version": pi_weatherstation.VERSION,
            "location": config.get("metrics_location_label"),
        }
        TEMPERATURE.set(labels, weather.get("temperature"))
        PRESSURE.set(labels, weather.get("pressure"))
        HUMIDITY.set(labels, weather.get("humidity"))
        GAS_RESISTANCE.set(labels, weather.get("gas_resistance"))
        if "air_quality" in weather:
            AIR_QUALITY.set(labels, weather.get("air_quality"))
