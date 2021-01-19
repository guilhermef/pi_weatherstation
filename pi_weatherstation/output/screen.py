import logging
import pathlib
import io

from jinja2 import Environment, PackageLoader, select_autoescape
import async_imgkit.api
import PIL.Image

try:
    import pi_weatherstation.output.display.ST7789_display as display
except ModuleNotFoundError:
    logging.warning("Problem loading display module, using debug display")
    import pi_weatherstation.output.display.debug_display as display

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
        self.display = display.Display()

    async def _render_image(self):
        rendered = template.render(
            resources_folder=RESOURCES_PATH,
            weather=self.store.get("weather_sensor"),
        )
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
        self.display.display_image(img_data)
        self.running = False
        logging.debug("Screen render done")

