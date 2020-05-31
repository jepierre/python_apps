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


def get_largest_odd_number(x, y, z):
    odd_array = []
    if check_odd(x):
        odd_array.append(x)
    if check_odd(y):
        odd_array.append(y)
    if check_odd(z):
        odd_array.append(z)

    if odd_array:
        return max(odd_array)
    else:
        raise ValueError("one of the numbers must be odd")


def print_largest_odd_number():
    input_numbers = []
    max_length = 10
    for number in range(max_length):
        x = input("enter number {} out of 10 numbers".format(number))
        if isinstance(x, int) and check_odd(x):
            input_numbers.append(x)

    if input_numbers:
        print("largest odd number: {}".format(max(input_numbers)))
    else:
        print("you must enter at least one odd number")


def squared_root_bisection(x):
    epsilon = 0.01
    num_guesses = 0
    low = 0.0
    high = max(1.0, x)
    ans = (high + low) / 2.0
    while abs(ans ** 2 - x) >= epsilon:
        print("low = {}, high = {}, ans = {}".format(low, high, ans))
        num_guesses += 1
        if ans ** 2 < x:
            low = ans
        else:
            high = ans
        ans = (high + low) / 2.0

    print("num_guesses = {}".format(num_guesses))
    print("{:.2f}, is close to square root of {}".format(ans, x))


def squared_root_newton_raphson(x):
    epsilon = 0.01
    num_guesses = 0
    guess = x / 2.0
    while abs(guess * guess - x) >= epsilon:
        guess = guess - (((guess ** 2) - x) / (2 * guess))
        print("guess = {}".format(guess))
        num_guesses += 1

    print("num_guesses = {}".format(num_guesses))
    print("{:1.02f}, is close to square root of {}".format(guess, x))


def sum_string(letter):
    numbers = letter.split(sep=",")
    print(numbers)
    print("sum of numbers: {}".format(sum([float(num) for num in numbers])))


def search(L, e):
    """Assumes L is a list, the elements of which are in ascending order.
       Returns True if e is in L and False otherwise."""

    def b_search(L, e, low, high):
        if high == low:
            return L[low] == e
        mid = (low + high) // 2
        if L[mid] == e:
            return True
        elif L[mid] > e:
            if low == mid:  # nothing left to search
                return False
            else:
                return b_search(L, e, low, mid - 1)
        else:
            return b_search(L, e, mid + 1, high)

    if len(L) == 0:
        return False
    else:
        return b_search(L, e, 0, len(L) - 1)


def check_odd(number):
    return not (number % 2 == 0)


def main():
    # print_largest_odd_number()
    number = 200001
    # squared_root_bisection(number)
    # squared_root_newton_raphson(number)
    sum_string("1.23,2.4,3.123,5.6")
    print(search([1, 2, 4, 5, 7, 9, 10], 10))


if __name__ == "__main__":
    main()
