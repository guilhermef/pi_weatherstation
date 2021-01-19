import logging
import asyncio

import async_cron.job as job
import async_cron.schedule as schedule

import pi_weatherstation.data.weather as weather_data
import pi_weatherstation.stores.memory as memory_store
import pi_weatherstation.output.screen as screen_output
import pi_weatherstation.metrics.pushgateway as metrics


class Daemon:
    def __init__(self):
        self.weather_data = weather_data.Weather(memory_store.store)
        self.screen = screen_output.ScreenOutput(memory_store.store)
        self.metrics = metrics.PushGatewayMetrics(memory_store.store)

    def start(self):
        logging.info("Starting daemon")
        loop = asyncio.get_event_loop()

        scheduler = schedule.Scheduler(check_interval=1, locale="en_US")

        scheduler.add_job(
            job.CronJob(name="update_weather")
            .every(1)
            .second.go(self.weather_data.update_weather)
        )

        scheduler.add_job(
            job.CronJob(name="render_screen")
            .every(1)
            .second.go(self.screen.output)
        )

        scheduler.add_job(
            job.CronJob(name="debug_store")
            .every(5)
            .second.go(self.show_store)
        )

        scheduler.add_job(
            job.CronJob(name="push_metrics")
            .every(5)
            .second.go(self.metrics.push_weather_data)
        )

        try:
            loop.run_until_complete(scheduler.start())
        finally:
            loop.run_until_complete(loop.shutdown_asyncgens())
            loop.close()

    async def show_store(self):
        logging.info(memory_store.store.stored_data)
