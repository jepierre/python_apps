#!/usr/bin/evn python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
""""
Author: Jean Pierre
Last Edited:

"""

# Python 2 compatible
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

# import
import unittest
from TDD.mycode import *

class MyFirstTests(unittest.TestCase):

    def test_hello(self):
        self.assertEqual(hello_world(), 'hello world')

    def test_custom_num_list(self):
        self.assertEqual(len(create_num_list(10)), 10)

    def test_custom_func_x(self):
        self.assertEqual(custom_func_x(3,2,3), 54)

    def test_custom_non_lin_num_list(self):
        self.assertEqual(custom_non_lin_num_list(5,2,3)[2], 16)
        self.assertEqual(custom_non_lin_num_list(5,3,2)[4], 48)

def main():
    unittest.main()

if __name__ == '__main__':
    unittest.main()