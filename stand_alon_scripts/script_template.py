import traceback
import termcolor
import logging
import os
import sys

PATH = os.path.dirname(__file__)
logger = logging.getLogger(__name__)


class EmptyClass:
    def __init__(self):
        pass


def setup_stream():
    # Turns on logging to console
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - "
        "<%(module)s:%(funcName)s:%(lineno)s> - %(message)s",
        "%Y-%m-%d %H:%M:%S",
    )
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    logger.setLevel(logging.DEBUG)


def catch_exceptions():
    # catches errors in gui and print them
    def excepthook(etype, value, tb):
        if isinstance(value, KeyboardInterrupt):
            sys.exit(1)
        else:
            termcolor.cprint("Sorry, something's wrong! ", "yellow", file=sys.stderr)
            # print traceback
            traceback.print_exception(etype, value, tb)

    # Set global exception handler.
    sys.excepthook = excepthook


def main():
    setup_stream()
    catch_exceptions()
    logger.debug("logger is working")


if __name__ == "__main__":
    main()
