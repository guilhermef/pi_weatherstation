# pi_weatherstation
Read the data from pimoroni BME680 and display on pimoroni SPI screen

## This project is still under development

## Dependencies:
* wkhtmltopdf(https://wkhtmltopdf.org/downloads.html)


## Install on RaspberryPI
* Enable SPI and I2C
```
sudo apt-get install python3-venv python3-dev libatlas-base-dev wkhtmltopdf libopenjp2-7

git clone git@github.com:guilhermef/pi_weatherstation.git

cd pi_weatherstation

python3 -m venv .env

source .env/bin/activate

# this will install the core dependencies
# and the dependencies for the screen st7789 and the sensor bme680

pip install -e .[st7789,bme680]

#run

pi_weatherstation -l debug
```
