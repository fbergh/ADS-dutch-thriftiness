### IMPORTS ###

# Standard library imports
import itertools

# Self-defined imports
from utils import *


### BRUTE-FORCE ALGORITHM ###

def brute_force(n_products, n_dividers, costs):
    """ Brute-force algorithm, for verification purposes """
    # Determine all possible arrangements of dividers (divider placed before the given index)
    divider_possibilities = []
    for used_dividers in range(0, n_dividers+1):
        divider_possibilities += itertools.combinations(range(1,n_products), used_dividers)

    # Initialize cost of best arrangement and a list for storing all equally good arrangements
    current_best = float("inf")
    best_arrangements = []
    # Loop through all possible arrangements
    for divider_arrangement in divider_possibilities:
        # Compute the cost corresponding to this arrangement
        cost = cost_of_checkout(split_costs(costs, divider_arrangement))
        # If the cost is better than the best cost, reset the best cost and store the current arrangement
        if cost < current_best:
            current_best = cost
            best_arrangements = [divider_arrangement]
        # If the cost is just as good as the best cost, add the arrangement to the list of best arrangements
        elif cost == current_best:
            best_arrangements += [divider_arrangement]

    # Return best arrangement(s)
    return current_best, best_arrangements


### GREEDY ALGORITHM ###

def greedy(n_products, n_dividers, costs):
    """ Solve the problem using a greedy strategy, after simplifying it """
    # Simplify the problem
    simple_n_products, simple_n_dividers, simple_costs, additional_cost = simplify_problem(n_products, n_dividers, costs)
    # If a very simple solution to the problem exists, return it
    simple_sol_works, simple_sol_cost = get_simple_solution(simple_n_products, simple_n_dividers, simple_costs)
    if simple_sol_works:
        return simple_sol_cost + additional_cost
    # Otherwise, return the "greedy" solution
    return _greedy(simple_n_products, simple_n_dividers, simple_costs) + additional_cost

def _greedy(n_products, n_dividers, costs, previous_choice=0):
    # If there are no products, return a cost of 0
    if n_products == 0:
        return 0
    # If there are no dividers, return the rounded sum of all costs
    if n_dividers == 0:
        return round_to_five(sum(costs))

    # Get index (and corresponding cost) of first gain of 2
    two_idx, two_cost = find_first_gain(costs, 2)
    # Get the "greedy" answer after the first gain of 2
    rem_two_cost, rem_two_gain= get_greedy_gain(n_products-two_idx, n_dividers-1, costs[two_idx:])
    # If this answer results in maximal gain, return the corresponding cost
    if rem_two_gain == n_dividers*2:
        return two_cost + rem_two_cost
    
    # Get index (and corresponding cost) of first gain of 1
    one_idx, one_cost = find_first_gain(costs, 1)
    # Get the "greedy" answer after the first gain of 1
    rem_one_cost, rem_one_gain = get_greedy_gain(n_products-one_idx, n_dividers-1 if previous_choice != 1 else n_dividers, costs[one_idx:])
    # If this answer results in maximal gain, return the corresponding cost
    if rem_one_gain == n_dividers*2:
        return one_cost + rem_one_cost

    # If the first gain of 1 occurs before the first gain of 2 and it does not reduce gain or increase cost, use it as the next divider position
    if one_idx < two_idx and (rem_one_gain >= rem_two_gain or one_cost + rem_one_cost <= two_cost + rem_two_cost):
        # If the previous choice also had a gain of 1, removing the divider there and adding it after this one results in a gain of 2
        if previous_choice == 1:
            return one_cost + _greedy(n_products-one_idx, n_dividers, costs[one_idx:], 2)
        # Otherwise, return the greedy solution after the gain of 1, noting that the current choice has a gain of 1
        return one_cost + _greedy(n_products-one_idx, n_dividers-1, costs[one_idx:], 1)
    # Otherwise, return the greedy solution after the gain of 2
    return two_cost + _greedy(n_products-two_idx, n_dividers-1, costs[two_idx:], 2)