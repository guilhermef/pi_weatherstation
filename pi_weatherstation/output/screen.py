import asyncio
import logging
import pathlib

from jinja2 import Environment, PackageLoader, select_autoescape
import async_imgkit.api
import PIL

import ST7789

RESOURCES_PATH = pathlib.Path(
    pathlib.Path(__file__).parent, "..", "template", "resources"
)

env = Environment(
    loader=PackageLoader("pi_weatherstation", "template"),
    autoescape=select_autoescape(["html"]),
)
template = env.get_template("index.html")


class ScreenOutput:
    def __init__(self, store):
        self.store = store
        self.running = False
        self.imgkit_config = async_imgkit.api.config()

    async def _render_image(self):
        rendered = template.render(resources_folder=RESOURCES_PATH)
        img = await async_imgkit.api.from_string(
            rendered,
            False,
            config=self.imgkit_config,
            options={
                "width": "240",
                "height": "240",
                "enable-local-file-access": "",
                "encoding": "UTF-8",
                "quiet": "",
            },
        )
        return img

    async def output(self):
        if self.running:
            logging.debug("Skipping, render already in progress")
        logging.debug("Screen render started")
        self.running = True
        img_data = await self._render_image()
        self._display_image(img_data)
        self.running = False
        logging.debug("Screen render done")

    def _display_image(self, img_data):
        pass
