import asyncio
import logging
import pathlib

from jinja2 import Environment, PackageLoader, select_autoescape
import async_imgkit.api

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

        with open("test.png", "wb") as f:
            f.write(img)
        return img

    async def output(self):
        if self.running:
            logging.debug("Skipping, render already in progress")
        logging.debug("Screen render started")
        self.running = True
        await self._render_image()
        self.running = False
        logging.debug("Screen render done")
