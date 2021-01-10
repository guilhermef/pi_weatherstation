import imgkit


class ScreenOutput:

    def __init__(self, weather_data):
        self.weather_data = weather_data

    def _html_template(self):
        return f"""
        <html>
            <body>
            <span>{self.weather_data.temperature}</span>
            <span>{self.weather_data.pressure}</span>
            <span>{self.weather_data.humidity}</span>
            </body>
        <html>
        """

    def _render_image(self):
        img = imgkit.from_string(
            self._html_template(),
            False
        )

        return img

    def output(self):
        self._render_image()
