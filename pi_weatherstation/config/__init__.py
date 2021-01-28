import configparser
import logging
import os

config = configparser.ConfigParser()
config.read_dict({
    "DEFAULT": {
        "enable_metrics": "true",
        "metrics_host": "0.0.0.0",
        "metrics_port": "9191",
        "enable_screen": "true",
        "metrics_location_label": "unknown",
    },
    "pi_weatherstation": {},
})


def init_config(config_path):
    files = config.read([
        config_path,
        os.path.expanduser('~/pi_weatherstation.ini')
    ])
    logging.info(f"Reading config files: {files}")


def getboolean(option, **kwargs):
    return config.getboolean("pi_weatherstation", option, **kwargs)


def getint(option, **kwargs):
    return config.getint("pi_weatherstation", option, **kwargs)


def get(option, **kwargs):
    return config.get("pi_weatherstation", option, **kwargs)
