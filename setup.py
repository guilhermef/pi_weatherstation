from setuptools import setup

from pi_weatherstation import VERSION


# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name="pi_weatherstation",
    version=VERSION,
    description="Read the data from pimoroni BME680 and display on pimoroni SPI screen",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="http://github.com/guilhermef/pi_weatherstation",
    author="Guilherme Souza",
    author_email="guilherme@souza.tech",
    license="MIT",
    packages=["pi_weatherstation"],
    install_requires=[
        "async-imgkit<1.0",
        "jinja2<3.0",
        "asyncio-periodic==2019.2",
        "aioprometheus[aiohttp]<21.0",
        "Pillow<9.0",
    ],
    extras_require={
        "st7789": [
            "st7789<1.0",
            "numpy<2.0",
            "spidev<4.0",
            "RPi.GPIO<1.0",
        ],
        "bme680": [
            "bme680<2.0",
            "smbus==1.1.post2",
        ]
    },
    zip_safe=False,
    entry_points={
        "console_scripts": ["pi_weatherstation=pi_weatherstation.cli:main"],
    },
)
