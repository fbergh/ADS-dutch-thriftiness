import random

def get_random_problem(n_products=None, force_fewer_dividers=False):
    """ Generate a random problem with the given number of products and a random number of dividers """
    if n_products == None:
        n_products = random.randint(1,10000)
    costs = [random.randint(1,50000) for _ in range(n_products)]
    n_dividers = random.randint(0, min(len(costs) - 1, 100) if force_fewer_dividers else 100)
    return n_products, n_dividers, costs

def get_simple_problems():
    """ Return a list of two 'simple' problems """
    costs_problems = [[10, 23, 43, 637, 45],
                      [1, 1, 1, 1, 1, 1],
                      [1, 2, 4, 8, 8, 3],
                      [2, 4, 3, 6, 7, 7],
                      [7, 7, 5, 1, 7, 7],
                      [6, 9, 3, 7, 2, 4]]
    n_dividers = [1, 2, 5, 5, 5, 5]
    n_products = [len(costs) for costs in costs_problems]
    return n_products, n_dividers, costs_problems

def get_hard_problems():
    """ Return a list of four 'hard' problems """
    costs_problems = [[2, 1, 2, 1, 2, 3],
                      [2, 2, 1, 2, 2, 1, 4, 4, 2, 3, 1, 2, 1, 3, 2, 3, 2, 3],
                      [2, 1, 2, 1, 2, 1, 1, 4, 2, 3, 3, 2, 4, 1, 3, 3],
                      [1, 3, 2, 2, 4, 1, 2, 1, 4, 3, 1, 1, 1, 2, 4],
                      [3, 4, 2, 2, 1, 2, 1, 1, 1, 3, 2, 2, 3, 4, 3, 3, 2, 3],
                      [4, 3, 4, 4, 4, 3, 3, 4, 3, 1, 3, 4, 4, 3, 1, 2, 2],
                      [2, 2, 3, 2, 4, 3, 1, 2, 1, 2, 4, 3, 3, 1, 2]]
    n_dividers = [4,5,13,16,12,10,11]
    n_products = [len(costs) for costs in costs_problems]
    return n_products, n_dividers, costs_problems