"""
Author: Jean-Elie Pierre
Date: 

based on examples from:
https://realpython.com/async-io-python/
https://hynek.me/articles/waiting-in-asyncio/

"""

# Imports
import logging
import os
import asyncio
import sys
import time
import traceback
import termcolor

# logger
logger = logging.getLogger(__name__)
PATH = os.path.dirname(__file__)


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


async def print_x(name, number, seconds):
    for i in range(number):
        # logger.debug("Task {} at number: {}".format(name, i))
        await asyncio.sleep(seconds)


func_args = [
    ("A", 100, 0.05),
    ("B", 100, 0.06),
    ("C", 100, 0.01),
    ("D", 100, 0.01),
    ("E", 100, 0.01),
    ("F", 100, 0.01),
]

async_funcs = [print_x(*func_arg) for func_arg in func_args]


async def master():
    tasks = [asyncio.create_task(function) for function in async_funcs]
    await asyncio.gather(*[task for task in tasks])


def print_x_no_async(name, number, seconds):
    for i in range(number):
        time.sleep(seconds)


def master_no_asyncio():
    [print_x_no_async(*func_arg) for func_arg in func_args]


def main():
    setup_stream()
    catch_exceptions()
    logger.debug("logger is working")

    start = time.perf_counter()
    asyncio.run(master())
    end = time.perf_counter()
    logger.debug("total time for asyncio: {}".format(end - start))

    start = time.perf_counter()
    master_no_asyncio()
    end = time.perf_counter()
    logger.debug("total time for regular function: {}".format(end - start))


if __name__ == "__main__":
    main()
