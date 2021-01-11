import pathlib

from jinja2 import Environment, PackageLoader, select_autoescape
import imgkit

RESOURCES_PATH = pathlib.Path(
    pathlib.Path(__file__).parent, "..", "template", "resources"
)

env = Environment(
    loader=PackageLoader("pi_weatherstation", "template"),
    autoescape=select_autoescape(["html"]),
)
template = env.get_template("index.html")


class ScreenOutput:
    def __init__(self, weather_data):
        self.weather_data = weather_data

    def _render_image(self):
        rendered = template.render(resources_folder=RESOURCES_PATH)
        img = imgkit.from_string(rendered, False, options={
            "width": "240",
            "height": "240",
            "enable-local-file-access": "",
            'encoding': "UTF-8",
        })

        with open("test.png", "wb") as f:
            f.write(img)
        return img

    def output(self):
        self._render_image()
