import random


def data_random(n_products):
    costs = [random.randint(1, 9) for _ in range(n_products)]
    n_dividers = random.randint(0, len(costs) - 1)
    return n_products, n_dividers, costs


def data_sample1():
    costs = [10, 23, 43, 637, 45]
    n_dividers = 1
    n_products = len(costs)
    return n_products, n_dividers, costs


def data_sample2():
    costs = [1, 1, 1, 1, 1, 1]
    n_dividers = 2
    n_products = len(costs)
    return n_products, n_dividers, costs


def get_difficult_problems():
    """
    Problems on which CheckoutCutting failed.
    Even when using all dividers (hence n_div=5 for all), it couldn't find the minimum. Very fishy
    """
    costs_problems = [[1, 2, 4, 8, 8, 3],
                      [2, 4, 3, 6, 7, 7],
                      [7, 7, 5, 1, 7, 7],
                      [6, 9, 3, 7, 2, 4]]
    n_dividers = [5, 5, 5, 5]
    n_products = [len(costs) for costs in costs_problems]
    return n_products, n_dividers, costs_problems