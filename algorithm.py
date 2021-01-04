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
    """ 
    Solve the problem using a greedy strategy, after simplifying it 
    
    Time complexity is O(n_products) + time complexity of _greedy 
    """
    simple_n_products, simple_n_dividers, simple_costs, additional_cost = simplify_problem(n_products, n_dividers, costs)
    return _greedy(simple_n_products, simple_n_dividers, simple_costs) + additional_cost

def _greedy(n_products, n_dividers, costs, previous_choice=0):
    # If there are no dividers, return the rounded sum of all costs
    if n_products == 0 or n_dividers == 0:
        return round_to_five(sum(costs))
    # If there is a simple solution to the problem, return that solution
    simple_sol_works, simple_sol_cost = get_simple_solution(n_products, n_dividers, costs)
    if simple_sol_works:
        return simple_sol_cost

    # Get index (and corresponding cost) of first gain of 2
    two_idx, two_cost = find_first_gain(costs, 2)
    # Get the "greedy" answer after the first gain of 2
    rem_two_cost, rem_two_gain= get_greedy_gain(n_products-two_idx, n_dividers-1, costs[two_idx:])
    # If this answer results in maximal gain, return the corresponding cost
    if rem_two_gain == (n_dividers+1)*2:
        return two_cost + rem_two_cost
    
    # Get index (and corresponding cost) of first gain of 1
    one_idx, one_cost = find_first_gain(costs, 1)
    # Get the "greedy" answer after the first gain of 1
    rem_one_cost, rem_one_gain = get_greedy_gain(n_products-one_idx, n_dividers-1 if previous_choice != 1 else n_dividers, costs[one_idx:])
    # If this answer results in maximal gain, return the corresponding cost
    if rem_one_gain == (n_dividers+1)*2:
        return one_cost + rem_one_cost

    if one_idx < two_idx and (rem_one_gain >= rem_two_gain or one_cost + rem_one_cost <= two_cost + rem_two_cost):
        if previous_choice == 1:
            return one_cost + _greedy(n_products-one_idx, n_dividers, costs[one_idx:], 2)
        return one_cost + _greedy(n_products-one_idx, n_dividers-1, costs[one_idx:], 1)
    return two_cost + _greedy(n_products-two_idx, n_dividers-1, costs[two_idx:], 2)


### BUGFIXING ###

# problems = []
# problems.extend([(10, 8, (1, 2, 1, 2, 1, 2, 2, 2, 1, 1))])
# problems.extend([(9, 5, (1, 2, 1, 2, 1, 4, 1, 1, 2)), (9, 6, (1, 2, 1, 2, 1, 4, 1, 1, 2)), (9, 7, (1, 2, 1, 2, 1, 4, 1, 1, 2)), (9, 8, (1, 2, 1, 2, 
# 1, 4, 1, 1, 2)), (9, 6, (1, 2, 4, 3, 1, 2, 2, 1, 1)), (9, 5, (1, 2, 1, 4, 4, 4, 1, 1, 2)), (9, 6, (1, 2, 1, 4, 4, 4, 1, 1, 2)), (9, 
# 7, (1, 2, 1, 4, 4, 4, 1, 1, 2)), (9, 8, (1, 2, 1, 4, 4, 4, 1, 1, 2)), (9, 5, (1, 2, 1, 3, 4, 1, 1, 3, 4)), (9, 5, (1, 2, 1, 3, 4, 1, 1, 4, 3)), (9, 6, (1, 2, 3, 1, 3, 1, 2, 2, 2)), (9, 7, (1, 2, 3, 1, 3, 1, 2, 2, 2)), (9, 8, (1, 2, 3, 1, 3, 1, 2, 2, 2)), (9, 6, (1, 2, 1, 3, 3, 1, 2, 2, 2)), (9, 7, (1, 2, 1, 3, 3, 1, 2, 2, 2)), (9, 8, (1, 2, 1, 3, 3, 1, 2, 2, 2)), (9, 5, (4, 2, 2, 1, 3, 4, 1, 1, 2)), (9, 6, (4, 2, 2, 1, 3, 4, 1, 1, 2)), (9, 7, (4, 2, 2, 1, 3, 4, 1, 1, 2)), (9, 8, (4, 2, 2, 1, 3, 4, 1, 1, 2)), (9, 5, (1, 2, 
# 1, 3, 4, 1, 4, 2, 2)), (9, 6, (1, 2, 1, 3, 4, 1, 4, 2, 2)), (9, 7, (1, 2, 1, 3, 4, 1, 4, 2, 2)), (9, 8, (1, 2, 1, 3, 4, 1, 4, 2, 2)), (9, 5, (1, 2, 3, 3, 3, 4, 1, 1, 2)), (9, 6, (1, 2, 3, 3, 3, 4, 1, 1, 2)), (9, 7, (1, 2, 3, 3, 3, 4, 1, 1, 2)), (9, 8, (1, 2, 3, 3, 3, 4, 1, 1, 2)), (9, 5, (3, 3, 2, 1, 3, 4, 1, 1, 2)), (9, 6, (3, 3, 2, 1, 3, 4, 1, 1, 2)), (9, 7, (3, 3, 2, 1, 3, 4, 1, 1, 2)), (9, 8, (3, 3, 2, 1, 3, 4, 1, 1, 2)), (9, 6, (1, 2, 4, 2, 2, 1, 2, 2, 2)), (9, 5, (1, 2, 4, 2, 2, 1, 2, 4, 3)), (9, 6, (1, 2, 4, 4, 4, 1, 2, 2, 2)), (9, 7, (1, 2, 4, 4, 4, 1, 2, 2, 2)), (9, 8, (1, 2, 4, 4, 4, 1, 2, 2, 2)), (9, 6, (1, 2, 4, 3, 1, 2, 2, 3, 4)), (9, 6, (4, 2, 2, 4, 3, 1, 2, 2, 2)), (9, 7, (4, 2, 2, 4, 3, 1, 2, 2, 2)), (9, 8, (4, 2, 2, 4, 3, 1, 2, 2, 2)), (9, 6, (3, 3, 2, 4, 3, 1, 2, 
# 2, 2)), (9, 7, (3, 3, 2, 4, 3, 1, 2, 2, 2)), (9, 8, (3, 3, 2, 4, 3, 1, 2, 2, 2))])
# problems.extend([(8, 7, (1, 2, 1, 3, 4, 1, 1, 2)), (8, 7, (1, 2, 1, 3, 4, 1, 1, 2)), (8, 7, (1, 2, 1, 3, 4, 1, 1, 2))])
# problems.extend([(7, 6, (3, 1, 4, 4, 2, 2, 2)), (7, 6, (2, 2, 3, 1, 4, 4, 2)), (7, 6, (2, 3, 1, 4, 4, 2, 2)), (7, 6, (2, 2, 2, 3, 1, 4, 4))] )
# problems.extend([(7, 6, (2, 2, 4, 4, 1, 3, 2)), (7, 6, (3, 1, 4, 4, 2, 2, 2)), (7, 6, (2, 2, 3, 1, 4, 4, 2)), (7, 6, (4, 4, 1, 3, 2, 2, 2)), (7, 6, 
# (2, 2, 2, 4, 4, 1, 3)), (7, 6, (2, 3, 1, 4, 4, 2, 2)), (7, 6, (2, 2, 2, 3, 1, 4, 4)), (7, 6, (2, 4, 4, 1, 3, 2, 2))])
# problems.extend([(2, 1, (4, 4)), (2, 1, (2, 3)), (2, 1, (1, 3)), (2, 1, (1, 4)), (2, 1, (2, 4))])
# problems.extend([(3, 2, (1, 2, 4))])
# problems.extend([(8, 6, (1, 2, 4, 3, 1, 2, 2, 2)), (8, 7, (1, 2, 4, 3, 1, 2, 2, 2)), (8, 5, (1, 2, 1, 3, 4, 1, 1, 2)), (8, 6, (1, 2, 1, 3, 4, 1, 1, 2)), (8, 7, (1, 2, 1, 3, 4, 1, 1, 2))])
# problems.extend([(8, 6, (1, 2, 4, 3, 1, 2, 2, 2)), (8, 7, (1, 2, 4, 3, 1, 2, 2, 2)), (8, 5, (1, 2, 1, 3, 4, 1, 1, 2)), (8, 6, (1, 2, 1, 3, 4, 1, 1, 2)), (8, 7, (1, 2, 1, 3, 4, 1, 1, 2))])
# problems.extend([(4, 1, (1, 2, 1, 1)), (4, 1, (1, 4, 3, 2)), (4, 1, (1, 2, 3, 4)), (4, 1, (1, 1, 1, 2)), (4, 1, (1, 3, 4, 2)), (4, 1, 
# (4, 2, 2, 2)), (4, 1, (1, 2, 2, 4)), (4, 1, (1, 4, 3, 1)), (4, 1, (4, 2, 2, 1)), (4, 1, (1, 2, 3, 3)), (4, 1, (1, 2, 4, 3)), (4, 1, (3, 3, 2, 2)), (4, 2, (2, 1, 2, 2)), (4, 1, (1, 3, 4, 1)), (4, 1, (3, 3, 2, 1)), (4, 2, (2, 1, 2, 1))])
# problems.extend([(8, 6, (1, 2, 4, 3, 1, 2, 2, 2)), (8, 7, (1, 2, 4, 3, 1, 2, 2, 2)), (8, 5, (1, 2, 1, 3, 4, 4, 3, 2)), (8, 6, (1, 2, 1, 3, 4, 4, 3, 2)), (8, 7, (1, 2, 1, 3, 4, 4, 3, 2)), (8, 5, (1, 2, 4, 3, 1, 2, 4, 3)), (8, 6, (1, 2, 4, 3, 1, 2, 4, 3)), (8, 7, (1, 2, 4, 3, 1, 2, 4, 3)), (8, 5, (1, 2, 1, 3, 4, 1, 1, 2)), (8, 6, (1, 2, 1, 3, 4, 1, 1, 2)), (8, 7, (1, 2, 1, 3, 4, 1, 1, 2)), (8, 4, (1, 2, 1, 3, 4, 2, 2, 3)), (8, 5, (1, 2, 1, 3, 4, 2, 2, 3)), (8, 6, (1, 2, 1, 3, 4, 2, 2, 
# 3)), (8, 7, (1, 2, 1, 3, 4, 2, 2, 3))])
# problems.extend([(7, 5, (1, 2, 1, 3, 4, 2, 2)), (7, 6, (1, 2, 1, 3, 4, 2, 2))])
# problems.extend([(4, 1, (1, 1, 1, 2)), (4, 1, (1, 2, 4, 3))])
# problems.extend([(8, 5, (1, 2, 4, 2, 2, 1, 2, 1)), (8, 5, (1, 2, 4, 2, 2, 1, 2, 2))])
# problems.extend([(8, 5, (1, 2, 1, 3, 4, 3, 4, 2)), (8, 6, (1, 2, 1, 3, 4, 3, 4, 2)), (8, 7, (1, 2, 1, 3, 4, 3, 4, 2)), (8, 3, (1, 4, 2, 4, 2, 2, 1, 2)), (8, 2, (1, 3, 3, 4, 2, 2, 4, 3)), (8, 3, (1, 4, 2, 4, 2, 2, 2, 2)), (8, 3, (1, 4, 2, 3, 3, 2, 2, 1)), (8, 6, (1, 2, 1, 2, 1, 4, 3, 1)), (8, 7, (1, 2, 1, 2, 1, 4, 3, 1)), (8, 6, (1, 2, 3, 3, 2, 1, 2, 1)), (8, 7, (1, 2, 3, 3, 2, 1, 2, 1)), (8, 5, (1, 2, 1, 2, 1, 1, 1, 1)), (8, 6, (1, 2, 1, 2, 1, 1, 1, 1)), (8, 5, (1, 2, 4, 2, 2, 1, 2, 
# 1)), (8, 6, (1, 4, 3, 1, 2, 1, 2, 1)), (8, 7, (1, 4, 3, 1, 2, 1, 2, 1)), (8, 6, (1, 2, 1, 2, 1, 2, 3, 3)), (8, 7, (1, 
# 2, 1, 2, 1, 2, 3, 3)), (8, 2, (1, 4, 2, 4, 2, 2, 4, 3)), (8, 5, (1, 2, 1, 2, 2, 4, 2, 1)), (8, 6, (1, 2, 1, 2, 2, 4, 2, 1)), (8, 7, (1, 2, 1, 2, 2, 4, 2, 1)), (8, 3, (1, 4, 2, 3, 3, 2, 2, 2)), (8, 6, (1, 2, 1, 4, 3, 1, 2, 1)), (8, 7, (1, 2, 1, 4, 3, 1, 2, 1)), (8, 3, (1, 3, 3, 3, 3, 2, 2, 1)), (8, 6, (3, 3, 2, 1, 2, 1, 2, 1)), (8, 7, (3, 3, 2, 1, 2, 1, 2, 1)), (8, 5, (1, 2, 1, 3, 4, 2, 1, 1)), (8, 6, (1, 2, 1, 3, 4, 2, 1, 1)), (8, 7, (1, 2, 1, 3, 4, 2, 1, 1)), (8, 3, 
# (1, 4, 2, 3, 3, 2, 1, 2)), (8, 6, (1, 3, 4, 1, 2, 1, 2, 1)), (8, 7, (1, 3, 4, 1, 2, 1, 2, 1)), (8, 6, (4, 2, 2, 1, 2, 
# 1, 2, 1)), (8, 7, (4, 2, 2, 1, 2, 1, 2, 1)), (8, 3, (1, 3, 3, 3, 3, 2, 2, 2)), (8, 5, (1, 2, 4, 2, 2, 1, 2, 2)), (8, 3, (1, 3, 3, 3, 3, 2, 1, 2)), (8, 6, (1, 2, 1, 2, 3, 3, 2, 1)), (8, 7, (1, 2, 1, 2, 3, 3, 2, 1)), (8, 2, (1, 4, 2, 3, 3, 2, 4, 3)), (8, 3, (1, 4, 2, 4, 2, 2, 2, 1)), (8, 3, (1, 3, 3, 4, 2, 2, 2, 1)), (8, 2, (1, 3, 3, 3, 3, 2, 4, 3)), (8, 3, (1, 3, 3, 4, 2, 2, 2, 2)), (8, 5, (1, 2, 1, 2, 1, 2, 4, 2)), (8, 6, (1, 2, 1, 2, 1, 2, 4, 2)), (8, 7, (1, 2, 1, 2, 1, 2, 4, 2)), (8, 3, (1, 3, 3, 4, 2, 2, 1, 2)), (8, 6, (1, 2, 1, 3, 4, 1, 2, 1)), (8, 7, (1, 2, 1, 3, 4, 1, 2, 1))])
# problems.extend([(8, 3, (1, 4, 2, 2, 1, 3, 1, 3)), (8, 5, (1, 2, 1, 2, 1, 2, 2, 3)), (8, 6, (1, 2, 1, 2, 1, 2, 2, 3)), (8, 7, (1, 2, 1, 2, 1, 2, 2, 3)), (8, 8, (1, 2, 1, 2, 1, 2, 2, 3)), (8, 3, (1, 3, 3, 2, 1, 3, 1, 3)), (8, 6, (1, 2, 1, 2, 1, 2, 2, 4)), (8, 7, (1, 2, 1, 2, 1, 2, 2, 4)), (8, 8, (1, 2, 1, 2, 1, 2, 2, 4))])
# problems.extend([(7, 4, (1, 3, 3, 2, 1, 2, 1)), (7, 4, (1, 3, 3, 2, 1, 2, 2)), (7, 4, (1, 4, 2, 2, 1, 2, 1)), (7, 4, (1, 4, 2, 2, 1, 2, 2))])


# mistakes = []
# for p in problems:
#     print(p)
#     n_products, n_dividers, costs = p
#     print("Brute Force:")
#     bf, bf_div = brute_force(n_products, n_dividers, costs)
#     print(bf, bf_div)
#     print("Greedy:")
#     g = greedy(n_products, n_dividers, costs)
#     print(g)
#     if bf != g:
#         mistakes.append(p)
#     print("\n----------\n")
# print(mistakes)
# print(f"made {len(mistakes)} mistakes out of {len(problems)}")