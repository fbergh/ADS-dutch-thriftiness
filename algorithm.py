### IMPORTS ###

# Standard library imports
import itertools

# Self-defined imports
from utils import *


### BRUTE-FORCE ALGORITHM ###

def brute_force(n_products, n_dividers, costs):
    """ Brute-force algorithm for determining optimal divider placements """
    # Determine all possible arrangements of dividers (divider placed before the given index)
    divider_possibilities = []
    for used_dividers in range(0, n_dividers+1):
        divider_possibilities += itertools.combinations(range(1,n_products), used_dividers)

    # Iterate through all arrangements to find the best ones
    current_best = float("inf")
    best_arrangements = []
    for divider_arrangement in divider_possibilities:
        checkout = split_costs(costs, divider_arrangement)
        cost = cost_of_checkout(checkout)
        if cost < current_best:
            current_best = cost
            best_arrangements = [divider_arrangement]
        elif cost == current_best:
            best_arrangements += [divider_arrangement]

    # Return best arrangement(s)
    return current_best, best_arrangements


### GREEDY ALGORITHM ###

def greedy(n_products, n_dividers, costs):
    """ Greedy algorithm (O(nk)?) """
    # Obtain the most greedy solution by splitting at all points where 2 cents can be saved
    greedy_sol = get_two_split(n_products, n_dividers, costs)
    # If this uses up all dividers, we are done
    if len(greedy_sol[1]) == n_dividers:
        return greedy_sol
    # Try to find the first point where 1 cent can be saved
    one_idx, one_cost = find_first(n_products, costs, 1)
    # If this point exists, check if putting a divider there it is beneficial
    if one_idx != n_products:
        new_greedy_sol = get_two_split(n_products-one_idx, n_dividers-1, costs[one_idx:])
        if len(new_greedy_sol[1]) >= len(greedy_sol[1]):
            rem_cost, rem_checkout = greedy(n_products-one_idx, n_dividers-1, costs[one_idx:])
            return (one_cost + rem_cost, [one_idx] + [one_idx + i for i in rem_checkout])
    # Otherwise, put a divider after the first point where 2 cents can be saved
    two_idx, two_cost = find_first(n_products, costs, 2)
    if two_idx != n_products:
        rem_cost, rem_checkout = greedy(n_products-two_idx, n_dividers-1, costs[two_idx:])
        return (two_cost + rem_cost, [two_idx] + [two_idx + i for i in rem_checkout])
    # If nothing has been returned yet, return the greedy solution
    return greedy_sol

# Example where greedy algorithm fails for now
n_products, n_dividers, costs = (6, 4, [2, 1, 2, 1, 2, 3])
print(brute_force(n_products, n_dividers, costs))
print(greedy(n_products, n_dividers, costs))