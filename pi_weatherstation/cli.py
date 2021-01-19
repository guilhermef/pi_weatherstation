import argparse
import logging

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
    import pi_weatherstation.runner.daemon as daemon
    runner = daemon.Daemon()
    runner.start()
