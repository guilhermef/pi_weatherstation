import asyncio
import logging
import time

import bme680


BURN_IN_TIME = 300

# The air quality algoithm is based on:
# https://github.com/pimoroni/bme680-python/blob/master/examples/indoor-air-quality.py


class Sensor:
    def __init__(self):
        self.sensor = self.configure_sensor()
        logging.debug("Initial reading:")
        for name in dir(self.sensor.data):
            value = getattr(self.sensor.data, name)

            if not name.startswith("_"):
                logging.debug("{}: {}".format(name, value))

        loop = asyncio.get_event_loop()
        self.gas_baseline = loop.create_future()
        loop.create_task(self.calculate_gas_baseline())

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
        sensor.set_gas_heater_temperature(320)
        sensor.set_gas_heater_duration(150)
        sensor.select_gas_heater_profile(0)
        return sensor

    async def get_sensor_data(self):
        data = {}
        if self.sensor.get_sensor_data():
            data.update(
                {
                    "temperature": self.sensor.data.temperature,
                    "pressure": self.sensor.data.pressure,
                    "humidity": self.sensor.data.humidity,
                }
            )
            if self.sensor.data.heat_stable:
                data.update({"gas_resistance": self.sensor.data.gas_resistance})
                if self.gas_baseline.done():
                    data.update(
                        {
                            "air_quality": self.calculate_air_quality(),
                        }
                    )

        return data

    async def calculate_gas_baseline(self):
        logging.info(
            f"Collecting gas resistance burn-in data for {BURN_IN_TIME} seconds"
        )
        temp_burn_in_data = []
        start_time = time.time()
        curr_time = time.time()

        while curr_time - start_time < BURN_IN_TIME:
            curr_time = time.time()
            if self.sensor.get_sensor_data() and self.sensor.data.heat_stable:
                gas = self.sensor.data.gas_resistance
                temp_burn_in_data.append(gas)
                logging.debug(f"Gas baseline calculation in progress: {gas} Ohms")
                await asyncio.sleep(1)
        gas_baseline = sum(temp_burn_in_data[-50:]) / 50.0

        logging.info(f"Gas baseline ready, air quality available: {gas_baseline}")

        self.gas_baseline.set_result(gas_baseline)

    def calculate_air_quality(self):
        gas_baseline = self.gas_baseline.result()
        # Set the humidity baseline to 40%, an optimal indoor humidity.
        hum_baseline = 40.0

        # This sets the balance between humidity and gas reading in the
        # calculation of air_quality_score (25:75, humidity:gas)
        hum_weighting = 0.25

        gas = self.sensor.data.gas_resistance
        gas_offset = gas_baseline - gas

        hum = self.sensor.data.humidity
        hum_offset = hum - hum_baseline

        # Calculate hum_score as the distance from the hum_baseline.
        if hum_offset > 0:
            hum_score = 100 - hum_baseline - hum_offset
            hum_score /= 100 - hum_baseline
            hum_score *= hum_weighting * 100

        else:
            hum_score = hum_baseline + hum_offset
            hum_score /= hum_baseline
            hum_score *= hum_weighting * 100

        # Calculate gas_score as the distance from the gas_baseline.
        if gas_offset > 0:
            gas_score = gas / gas_baseline
            gas_score *= 100 - (hum_weighting * 100)

        else:
            gas_score = 100 - (hum_weighting * 100)

        # Calculate air_quality_score.
        air_quality_score = hum_score + gas_score

        return air_quality_score
