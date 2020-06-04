#!/usr/bin/evn python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
""""
Author: Jean Pierre
Last Edited:

to run:
    python -m unittest -v test_mycode.py
"""

# Python 2 compatible
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import unittest
from IntroToComputationAndProgramming import *


class MyTests(unittest.TestCase):
    def test_get_largest_odd_number(self):
        self.assertEqual(get_largest_odd_number(x=10, y=20, z=9), 9, msg="my message")


def main():
    unittest.main()


if __name__ == "__main__":
    main()
