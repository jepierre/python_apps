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


def hello_world():
    return "hello world"


def create_num_list(length):
    return [x for x in range(length)]


def custom_func_x(x, const, power):
    return const * x ** power


def custom_non_lin_num_list(length, const, power):
    return [custom_func_x(x, const, power) for x in range(length)]


def main():
    pass


if __name__ == "__main__":
    main()
