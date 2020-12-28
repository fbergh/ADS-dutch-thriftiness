import random

def get_random_problem(n_products):
    """ Generate a random problem with the given number of products and a random number of dividers """
    costs = [random.randint(1,9) for _ in range(n_products)]
    n_dividers = random.randint(0, len(costs) - 1)
    return n_products, n_dividers, costs

def get_simple_problems():
    """ Return a list of two 'simple' problems """
    costs_problems = [[10, 23, 43, 637, 45],
                      [1, 1, 1, 1, 1, 1]]
    n_dividers = [1, 2]
    n_products = [len(costs) for costs in costs_problems]
    return n_products, n_dividers, costs_problems

def get_hard_problems():
    """ Return a list of four 'hard' problems """
    costs_problems = [[1, 2, 4, 8, 8, 3],
                      [2, 4, 3, 6, 7, 7],
                      [7, 7, 5, 1, 7, 7],
                      [6, 9, 3, 7, 2, 4]]
    n_dividers = [5, 5, 5, 5]
    n_products = [len(costs) for costs in costs_problems]
    return n_products, n_dividers, costs_problems