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
        "imgkit",
    ],
    zip_safe=False,
    entry_points={
        "console_scripts": ["pi_weatherstation=pi_weatherstation.cli:main"],
    },
)
