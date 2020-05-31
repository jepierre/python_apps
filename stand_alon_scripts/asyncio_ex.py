"""
Author: Jean-Elie Pierre
Date: 

"""

# Imports

import logging
import os
import asyncio

# set up logger
import time

logger = logging.getLogger("root")
logger.setLevel(logging.DEBUG)

# Paths
PATH = os.path.dirname(__file__)


def main(*args):
    # Turns on logging to console
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - <%(funcName)s:%(lineno)s> - %(message)s",
        "H",
    )
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    async def print_x(name, number, seconds):
        for i in range(number):
            print("Task {} at number: {}".format(name, i))
            await asyncio.sleep(seconds)

    start = time.time()
    my_event_loop = asyncio.get_event_loop()
    tasks = [
        asyncio.ensure_future(print_x("A", number=10, seconds=2)),
        asyncio.ensure_future(print_x("B", number=15, seconds=1)),
    ]

    my_event_loop.run_until_complete(asyncio.wait(tasks))
    my_event_loop.close()

    end = time.time()
    logger.debug("total time: {}".format(end - start))


if __name__ == "__main__":
    main()
