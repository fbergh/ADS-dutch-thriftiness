import math


# Hard-coded dictionary for value of the last digit of a number modulo 5
# E.g. 3 will be rounded to 5, so it costs 2 more. Therefore, ADDED_VALUE_DICT[3]=-2
# -1 maps to -inf as a utility for the algorithm
VALUE_DICT = {-1: -math.inf, 0: 0, 1: 1, 2: 2, 3: -2, 4: -1}


def round_to_5(x):
    return 5 * round(x/5)


def do_add_product(product, cur_cost):
    return value(product + cur_cost) > value(cur_cost)


def value(cost):
    # % 10, because we want last digit. % 5, because values in VALUE_DICT are the same after 4
    return VALUE_DICT[cost % 10 % 5]
