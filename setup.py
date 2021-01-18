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
        "opentsdb-py<1.0",
        "aioprometheus[aiohttp]<21.0",
    ],
    zip_safe=False,
    entry_points={
        "console_scripts": ["pi_weatherstation=pi_weatherstation.cli:main"],
    },
)
