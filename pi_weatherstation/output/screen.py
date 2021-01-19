import logging
import pathlib
import io

from jinja2 import Environment, PackageLoader, select_autoescape
import async_imgkit.api
import PIL.Image

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
        self.display = ST7789.ST7789(
            port=0,
            cs=ST7789.BG_SPI_CS_FRONT,  # BG_SPI_CS_BACK or BG_SPI_CS_FRONT
            dc=9,
            backlight=19,               # 18 for back BG slot, 19 for front BG slot.
            spi_speed_hz=80 * 1000 * 1000
        )
        self.display.begin()

    async def _render_image(self):
        rendered = template.render(resources_folder=RESOURCES_PATH)
        img = await async_imgkit.api.from_string(
            rendered,
            False,
            config=self.imgkit_config,
            options={
                "format": "png",
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
        image = PIL.Image.open(io.BytesIO(img_data))
        self.display.display(image)

