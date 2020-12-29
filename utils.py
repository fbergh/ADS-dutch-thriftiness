### GENERAL UTILITIES ###

def round_to_five(x):
    """ Round integer x to the nearest multiple of 5 """
    return 5 * round(x/5)


### BRUTE-FORCE UTILITIES ###

def cost_of_checkout(checkout):
    """ Compute cost of checkout list """
    return sum([round_to_five(sum(part)) for part in checkout])

def split_costs(costs, divider_positions):
    """ Split given list of costs according to given divider positions """
    # Add first index of first split and last index of last split
    divider_positions = [0] + list(divider_positions) + [len(costs)]
    # Split costs according to divider positions
    checkouts = [costs[divider_positions[i]:divider_positions[i+1]] for i in range(0, len(divider_positions)-1)]
    # Return the list of checkouts
    return checkouts


### GREEDY UTILITIES ###

def get_two_split(n_products, n_dividers, costs):
    """ Get the checkout if we split only when we can save two cents (O(n))"""
    # Initialize accumulator and solution values
    acc_cost = 0
    sol_cost, sol_checkout = 0, []
    # Iterate through the list of costs and split where possible
    for i, c in enumerate(costs):
        acc_cost += c
        if (n_dividers > 0 and acc_cost % 5 == 2) or i == n_products-1:
            sol_cost += round_to_five(acc_cost)
            acc_cost = 0
            n_dividers -= 1
            if i < n_products-1:
                sol_checkout.append(i+1)
    # Return the solution
    return (sol_cost, sol_checkout)

def find_first(n_products, costs, gain):
    acc_cost = 0
    for i, c in enumerate(costs):
        acc_cost += c
        if acc_cost % 5 == gain:
            return i+1, round_to_five(acc_cost)
    return n_products, round_to_five(acc_cost)