import argparse
import logging

import pi_weatherstation
import pi_weatherstation.config as config


parser = argparse.ArgumentParser()
parser.add_argument(
    "-l",
    "--loglevel",
    default="warning",
    help="Provide logging level. Example --loglevel debug, default=warning",
)

parser.add_argument(
    "-v", "--version", help="Show version and exit", action="store_true"
)

parser.add_argument(
    "-c",
    "--config",
    help="Config file path. Example '/etc/pi_weatherstation/config.ini'",
    default="pi_weatherstation.ini",
)

args = parser.parse_args()

logging.basicConfig(
    format="[%(levelname)s][%(module)s]:%(message)s", level=args.loglevel.upper()
)


def main():
    if args.version:
        print(f"pi_weatherstation: {pi_weatherstation.VERSION}")
        return

    config.init_config(args.config)

    import pi_weatherstation.runner.daemon as daemon

    runner = daemon.Daemon()
    runner.start()
