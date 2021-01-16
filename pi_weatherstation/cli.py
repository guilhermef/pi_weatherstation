import argparse
import logging

import pi_weatherstation.runner.daemon as daemon

parser = argparse.ArgumentParser()
parser.add_argument(
    "-l",
    "--loglevel",
    default="warning",
    help="Provide logging level. Example --loglevel debug, default=warning",
)

args = parser.parse_args()

logging.basicConfig(
    format="[pi_weatherstation][%(levelname)s]:%(message)s", level=args.loglevel.upper()
)


def main():
    runner = daemon.Daemon()
    runner.start()
