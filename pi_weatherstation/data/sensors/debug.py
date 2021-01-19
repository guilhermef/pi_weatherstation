class Sensor:

    async def get_sensor_data(self):
        return {
            "temperature": 50,
            "pressure": 500,
            "humidity": 50,
            "gas_resistance": 500,
        }
