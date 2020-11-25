import sys

def get_values_from_input():
    """
    From the assignment:
    You are given the following data (via stdin):
        - One line with the number of products: n (1 <= n <= 2500) and the number of dividers: k (0 <= k <= 25).
        (The upper bounds on the number of products and dividers are tentative, and be changed the coming weeks.)
        - One line with all the n costs in cents: c_1, ..., c_n cn (1 <= c_i <= 50000).
        The products come in order they are put on the conveyor belt (so c_1 is closest to the cashier).
    """
    n_prod_div_str = input().split(" ")
    n_products, n_dividers = int(n_prod_div_str[0]), int(n_prod_div_str[1])
    assert 1 <= n_products <= 2500, "Number of products should be in range [1,2500]"
    assert 0 <= n_dividers <= 25, "Number of products should be in range [0,25]"

    costs_str = input().split(" ")
    costs = [int(cost_str) for cost_str in costs_str]
    assert len(costs) == n_products, "Each product should have one cost"
    assert all([1 <= cost <= 50000 for cost in costs]), "Each cost should be in range [1,50000]"

    return n_products, n_dividers, costs


def eprint(*args, **kwargs):
    """ Print to stderror (which logs to console for testing server) """
    print(*args, file=sys.stderr, **kwargs)


def send(cost):
    print(cost)