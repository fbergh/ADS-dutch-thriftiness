import random


def data_random(n_products):
    costs = [random.randint(1, 10) for _ in range(n_products)]
    n_dividers = random.randint(0, 25)
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