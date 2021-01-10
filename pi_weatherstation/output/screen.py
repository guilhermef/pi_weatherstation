import tempfile
import pathlib

from jinja2 import Environment, PackageLoader, select_autoescape
from selenium import webdriver

RESOURCES_PATH = pathlib.Path(
    pathlib.Path(__file__).parent, "..", "template", "resources"
)

env = Environment(
    loader=PackageLoader("pi_weatherstation", "template"),
    autoescape=select_autoescape(["html"]),
)

template = env.get_template("index.html")

options = webdriver.ChromeOptions()
options.add_argument("--window-size=240,240")
options.add_argument("--headless")
options.add_argument("--force-device-scale-factor=1.0")
driver = webdriver.Chrome(options=options)
driver.set_window_position(0, 0)
driver.set_window_size(240, 240)


class ScreenOutput:
    def __init__(self, weather_data):
        self.weather_data = weather_data

    def _render_image(self):
        with tempfile.NamedTemporaryFile(mode="w+", suffix=".html") as f:
            template.stream(resources_folder=RESOURCES_PATH).dump(f)
            f.seek(0)
            driver.get(f"file://{f.name}")
            driver.get_screenshot_as_file("test.png")
            img = driver.get_screenshot_as_png()
        return img

    def output(self):
        self._render_image()
