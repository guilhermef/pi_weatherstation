import logging
import asyncio

import periodic

import pi_weatherstation.data.weather as weather_data
import pi_weatherstation.stores.memory as memory_store
import pi_weatherstation.output.screen as screen_output
import pi_weatherstation.metrics.prometheus as metrics


class Daemon:
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.weather_data = weather_data.Weather(memory_store.store)
        self.screen = screen_output.ScreenOutput(memory_store.store)
        self.metrics = metrics.PrometheusMetrics(memory_store.store)

    def start(self):
        logging.info("Starting daemon")
        try:
            self.loop.run_until_complete(self.metrics.start_prometheus_server())
            self.loop.create_task(self.start_tasks())
            self.loop.create_task(self.on_weather_updated_event())
            self.loop.run_forever()
        finally:
            self.loop.run_until_complete(self.loop.shutdown_asyncgens())
            self.loop.close()

    async def start_tasks(self):
        update_weather = periodic.Periodic(
            5, self.weather_data.update_weather
        )
        await update_weather.start()

    async def on_weather_updated_event(self):
        while True:
            try:
                await memory_store.store.ready.wait()
                await self.screen.output()
                await self.metrics.push_weather_data()
                await self.show_store()
            except Exception as e:
                logging.error(e)

    async def show_store(self):
        logging.info(memory_store.store.stored_data)
