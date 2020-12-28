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


### "GREEDY" TWO-CHOICES ALGORITHM ###

def greedy_two_choices(n_products, n_dividers, costs):
    """ 'Greedy' algorithm that considers two greedy choices at each step """
    # Set parameters
    reached_one = False
    reached_two = False
    total_cost = round_to_five(sum(costs))
    solution_one = (total_cost, [])
    solution_two = (total_cost, [])
    first_cost = 0
    index = 1
    
    # Find first +1 and first +2
    while not (reached_one and reached_two) and not index == n_products and n_dividers > 0:
        first_cost += costs[index-1]
        items_remaining = n_products - index
        if first_cost % 5 == 1:
            reached_one = True
            rem_cost, rem_arrangement = greedy_two_choices(items_remaining, n_dividers-1, costs[index:])
            solution_one = (round_to_five(first_cost) + rem_cost, [index]+[index+i for i in rem_arrangement])
        if first_cost % 5 == 2:
            reached_two = True
            rem_cost, rem_arrangement = greedy_two_choices(items_remaining, n_dividers-1, costs[index:])
            solution_two = (round_to_five(first_cost) + rem_cost, [index]+[index+i for i in rem_arrangement])
        index += 1

    # Return the best solution
    best_solution = solution_one if solution_one[0] <= solution_two[0] else solution_two
    return best_solution