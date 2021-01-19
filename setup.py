from setuptools import setup

setup(
    name="pi_weatherstation",
    version="0.1",
    description="Read the data from pimoroni BME680 and display on pimoroni SPI screen",
    url="http://github.com/guilhermef/pi_weatherstation",
    author="Guilherme Souza",
    author_email="guilherme@souza.tech",
    license="MIT",
    packages=["pi_weatherstation"],
    install_requires=[
        "async-imgkit<1.0",
        "jinja2<3.0",
        "async-cron<2.0",
        "aioprometheus[aiohttp]<21.0",
        "Pillow<9.0",
        # st7789 dependencies
        "st7789<1.0",
        "numpy<2.0",
        "spidev<4.0",
        "RPi.GPIO<1.0",
    ],
    zip_safe=False,
    entry_points={
        "console_scripts": ["pi_weatherstation=pi_weatherstation.cli:main"],
    },
)
