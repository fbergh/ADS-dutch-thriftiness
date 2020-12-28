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


### TWO-CHOICE UTILITIES ###