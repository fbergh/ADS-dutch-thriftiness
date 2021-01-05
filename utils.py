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

def simplify_problem(n_products, n_dividers, costs):
    """
    Simplify a problem by removing costs that are multiples of 5 and reducing costs to only include 
    the parts where saving can actually occur (additional cost needs to be added back afterwards)
    """
    # Initialize values for simplified problem
    new_n_products, new_costs, additional_cost = 0, [], 0
    # Loop through list of costs
    for c in costs:
        # Round down the cost to the nearest multiple of 5
        rounded_down = int(c/5)*5
        # Add this rounded value to the additional cost
        additional_cost += rounded_down
        # If the remainder is more than 0, add it to the simplified problem
        if c - rounded_down > 0:
            new_n_products += 1
            new_costs.append(c - rounded_down)
    # Return the simplified problem and the additional cost
    return new_n_products, min(n_dividers, new_n_products-1), new_costs, additional_cost

def get_simple_solution(n_products, n_dividers, costs):
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
        # If a 1 or a 2 occurs by itself (resulting in a gain of 1 or 2), place a divider directly after it
        elif costs[i] == 1 or costs[i] == 2:
            n_dividers -= 1
        # If any other number occurs by itself, no simple solution exists
        elif costs[i] > 0:
            return False, None
        i += 1
    # If the final index happens to be the last item, add the rounded cost of that item to the total cost
    if i == n_products-1:
        total_cost += round_to_five(costs[n_products-1])
    # Return whether a simple solution exists (the final product can be reached by placing dividers in an obvious manner) and the total cost of that simple solution
    return i >= n_products-1, total_cost


def get_greedy_gain(n_products, n_dividers, costs):
    # If the list of costs is empty, return a cost and a gain of 0
    if not costs:
        return 0, 0
    # Initialize values for accumulator and index of last divider
    accumulator, last_divider_idx = 0,0
    # Initialize values for first gain of 1 after the last divider and the corresponding cost 
    first_one_idx, first_one_cost = 0,0
    # Initialize result values
    total_cost, total_gain = 0,0

    # Loop through the list of costs
    i = 0
    while i <= n_products:
        # If we have arrived at the end:
        if i == n_products:
            # If possible, go back to the first gain of 1 after the last divider (note: this can happen at most twice!)
            if first_one_idx > last_divider_idx and n_dividers > 0 and first_one_idx < n_products:
                total_cost += first_one_cost
                last_divider_idx = first_one_idx
                n_dividers -= 1
                total_gain += 1
                accumulator = 0
                i = last_divider_idx
            # Otherwise, return the result
            else:
                total_cost += round_to_five(accumulator)
                total_gain += accumulator % 5 if accumulator % 5 <= 2 else accumulator % 5 - 5
                return total_cost, total_gain

        # If we are not at the end, add the current cost to the accumulator
        accumulator += costs[i]
        # If a gain of one is found and no such gain has been found since the last divider, set the position of a gain of one to this index
        if accumulator % 5 == 1 and first_one_idx < last_divider_idx:
            first_one_idx = i+1
            first_one_cost = round_to_five(accumulator)
        # Otherwise, if a gain of 2 is found, "put a divider" after this index
        elif accumulator % 5 == 2 and n_dividers > 0:
            total_cost += round_to_five(accumulator)
            last_divider_idx = i+1
            n_dividers -= 1
            total_gain += 2
            accumulator = 0

        # Go to the next item in the list
        i += 1
    

def find_first_gain(costs, gain):
    """ 
    Find the first occurrence of the specified gain (1 or 2)
    """
    # Initialize accumulator
    accumulator = 0
    # Loop through costs; if the correct gain is found, return the next index
    for i,c in enumerate(costs):
        accumulator += c
        if accumulator % 5 == gain:
            return i+1, accumulator-gain
    # If the gain was not found, return the length of costs
    return len(costs), round_to_five(accumulator)