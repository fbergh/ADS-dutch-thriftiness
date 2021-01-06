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


### "SIMPLE OR GREEDY" ALGORITHM ###

def simple_or_greedy(n_products, n_dividers, costs):
    """ Solve the problem using the "simple or greedy" strategy, after simplifying it """
    # Simplify the problem
    simple_n_products, simple_n_dividers, simple_costs, additional_cost = simplify_problem(n_products, n_dividers, costs)
    # If a "simple" solution to the problem exists, return it
    simple_sol_works, simple_sol_cost = _simple(simple_n_products, simple_n_dividers, simple_costs)
    if simple_sol_works:
        return simple_sol_cost + additional_cost
    # Otherwise, return the "greedy" solution
    return _greedy(simple_n_products, simple_n_dividers, simple_costs) + additional_cost


def _simple(n_products, n_dividers, costs):
    """ Checks if a simple solution exists for this problem, and if so, returns it """
    # Initialize value that keeps track of total cost and append a 0 to costs (simple way to deal with out-of-bounds look-ahead)
    total_cost = 0
    costs.append(0)

    # Loop through the list of costs
    i = 0
    while i <= n_products and n_dividers > 0:
        # If two 1s occur in succession (resulting in a gain of 2), add a divider after the second 1
        if costs[i] == 1 and costs[i+1] == 1:
            n_dividers -= 1
            i += 1
        # If a 1, 4 and 4 occur in succession (resulting in a gain of 2), and the 4 is not followed by a 3, add a divider after the 4
        elif costs[i] == 1 and costs[i+1] == 2 and costs[i+2] == 4 and costs[i+3] != 3:
            total_cost += 5
            n_dividers -= 1
            i += 2
        # If a 4 is followed by a 3 (resulting in a gain of 2), add a divider after the 3 and record a cost of 5
        elif costs[i] == 4 and costs[i+1] == 3 or costs[i] == 3 and costs[i+1] == 4:
            total_cost += 5
            n_dividers -= 1
            i += 1
        # If a 3 is followed by a 3 (resulting in a gain of 1), place a divider after the second 3 and record a cost of 5
        elif costs[i] == 3 and costs[i+1] == 3:
            total_cost += 5
            n_dividers -= 1
            i += 1
        # If a 4 is followed by a 2 (resulting in a gain of 1), place a divider directly after it
        elif costs[i] == 4 and costs[i+1] == 2 or costs[i] == 2 and costs[i+1] == 4 and costs[i+2] != 3:
            total_cost += 5
            n_dividers -= 1
            i += 1
        # If a 1 or a 2 occurs by itself (resulting in a gain of 1 or 2), place a divider directly after it
        elif costs[i] == 1 or costs[i] == 2:
            n_dividers -= 1
        # If any other number occurs by itself, no simple solution exists
        elif costs[i] > 0:
            return False, None
        i += 1
    # If no dividers are left but the final two products can be "combined" like above, do so
    if i == n_products-2:
        if costs[i] == 1 and costs[i+1] == 1:
            i += 1
        elif costs[i] == 3 and costs[i+1] == 3:
            total_cost += 5
            i += 1
        elif costs[i] == 3 and costs[i+1] == 4 or costs[i] == 4 and costs[i+1] == 3:
            total_cost += 5
            i += 1
        elif costs[i] == 4 and costs[i+1] == 2 or costs[i] == 2 and costs[i+1] == 4:
            total_cost += 5
            i += 1
    # Otherwise, if the final index happens to be the last item, add the rounded cost of that item to the total cost
    elif i == n_products-1:
        total_cost += round_to_five(costs[n_products-1])
    # Return whether a simple solution exists (the final product can be reached by placing dividers in an obvious manner) and the total cost of that simple solution
    return i >= n_products-1, total_cost


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
    rem_two_cost, rem_two_gain = get_greedy_gain(n_products-two_idx, n_dividers-1, costs[two_idx:])
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