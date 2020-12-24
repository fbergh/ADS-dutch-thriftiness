import math


# Hard-coded dictionary for value of the last digit of a number modulo 5
# E.g. 3 will be rounded to 5, so it costs 2 more. Therefore, ADDED_VALUE_DICT[3]=-2
# -1 maps to -inf as a utility for the algorithm
GAIN_DICT = {-1: -math.inf, 0: 0, 1: 1, 2: 2, 3: -2, 4: -1}


def round_to_5(x):
    return 5 * round(x/5)


def do_add_product(product, cur_cost):
    return gain(product + cur_cost) > gain(cur_cost)


def gain(cost):
    # % 10, because we want last digit. % 5, because values in VALUE_DICT are the same after 4
    return GAIN_DICT[cost % 10 % 5] if cost != -1 else GAIN_DICT[cost]


def cost_of_checkout(checkout):
    return sum([round_to_5(cost)for cost in checkout])


def get_mod_5_values(costs):
    mod_5_values = []
    for i in reversed(range(len(costs))):
        if costs[i] % 5 == 0:
            mod_5_values.append(costs.pop(i))
    return mod_5_values
