### IMPORTS ###

# Standard library imports
import random
import itertools


### GENERATING EXAMPLE PROBLEMS ###

def get_random_problem(n_products=None, force_fewer_dividers=False):
    """ Generate a random problem with the given number of products and a random number of dividers """
    # If the number of products is unspecified, generate it randomly, within the bounds of the assignment
    if n_products == None:
        n_products = random.randint(1,10000)
    # Generate random costs for each product, within the bounds of the assignment
    costs = [random.randint(1,50000) for _ in range(n_products)]
    n_dividers = random.randint(0, min(len(costs) - 1, 100) if force_fewer_dividers else 100)
    return n_products, n_dividers, costs


def get_all_problems(n_products=5):
    """ Generates all possible distinct problems with the given number of products """
    # Initialize list for storing all problems
    problems = []
    # Retrieve all distinct ordered combinations of values from [1,2,3,4]
    all_sets = itertools.combinations_with_replacement([1,2,3,4], n_products)
    # For each of these ordered sets, store all permutations of this set with all possible numbers of dividers
    for s in all_sets:
        all_costs = list(set([costs for costs in itertools.permutations(s)]))
        for costs in all_costs:
            for n_dividers in range(n_products):
                problems.append((n_products, n_dividers, costs))
    # Return the created list of problems
    return problems