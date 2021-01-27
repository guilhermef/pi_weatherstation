class Sensor:

    async def get_sensor_data(self):
        return {
            "temperature": 50,
            "pressure": 500,
            "humidity": 30,
            "gas_resistance": 500,
        }
