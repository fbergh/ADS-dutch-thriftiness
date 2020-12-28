### IMPORTS ###

# Self-defined imports
from algorithm import *
from example_problems import *


### OFFLINE TESTING ###
simple_problems = get_simple_problems()
hard_problems = get_hard_problems()

# Test simple problems
n_products, n_dividers, costs_problems = simple_problems
for i in range(len(n_products)):
    print(f"Testing simple problem {i+1}")
    print(f"Brute force: {brute_force(n_products[i], n_dividers[i], costs_problems[i])}")
    print(f"Greedy two choices: {greedy_two_choices(n_products[i], n_dividers[i], costs_problems[i])}")

# Test hard problems
n_products, n_dividers, costs_problems = hard_problems
for i in range(len(n_products)):
    print(f"Testing hard problem {i+1}")
    print(f"Brute force: {brute_force(n_products[i], n_dividers[i], costs_problems[i])}")
    print(f"Greedy two choices: {greedy_two_choices(n_products[i], n_dividers[i], costs_problems[i])}")