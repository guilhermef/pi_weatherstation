import pi_weatherstation.output.screen as screen
import pi_weatherstation.data.weather as weather_data


def main():
    weather = weather_data.Weather()
    screen.ScreenOutput(weather).output()
