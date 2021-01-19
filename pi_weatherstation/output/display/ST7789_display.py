import io

import PIL.Image
import ST7789


class Display:
    def __init__(self):
        self.display = ST7789.ST7789(
            port=0,
            cs=ST7789.BG_SPI_CS_FRONT,  # BG_SPI_CS_BACK or BG_SPI_CS_FRONT
            dc=9,
            backlight=19,               # 18 for back BG slot, 19 for front BG slot.
            spi_speed_hz=80 * 1000 * 1000
        )
        self.display.begin()

    def display_image(self, img_data):
        image = PIL.Image.open(io.BytesIO(img_data))
        self.display.display(image)
