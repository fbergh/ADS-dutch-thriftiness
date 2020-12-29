### IMPORTS ###

# Standard library imports
import time

# Self-defined imports
from algorithm import *
from example_problems import *


### CONSTANTS ###

TEST_SIMPLE = False
TEST_HARD = False
TEST_RANDOM = True

VERIFY_BRUTEFORCE = True


### CORRECTNESS COUNTERS ###
n_problems = 0
n_correct = 0


### OFFLINE TESTING ###

def test_algorithm(problem, algorithm, algorithm_name):
    n_products, n_dividers, costs = problem
    start_time = time.time()
    cost, checkout = algorithm(n_products, n_dividers, costs)
    end_time = time.time()
    print(f"{algorithm_name}: {cost} ({end_time-start_time:.3f} seconds)")
    return cost, checkout

def test_problem(problem):
    global n_problems
    n_problems += 1
    if VERIFY_BRUTEFORCE:
        solution = test_algorithm(problem, brute_force, "Brute force")
    answer = test_algorithm(problem, greedy, "Greedy")
    if VERIFY_BRUTEFORCE:
        correct = answer[0] == solution[0]
        print("CORRECT" if correct else "INCORRECT")
        global n_correct
        n_correct += 1 if correct else 0
        if answer[0] != solution[0]:
            print(problem)
    print("")


if __name__ == "__main__":

    # Test simple problems
    if TEST_SIMPLE:
        print("Testing simple problems\n")
        n_products, n_dividers, costs_problems = get_simple_problems()
        for i in range(len(n_products)):
            print(f"Testing simple problem {i+1}")
            problem = (n_products[i], n_dividers[i], costs_problems[i])
            test_problem(problem)

    # Test hard problems
    if TEST_HARD:
        print("Testing hard problems\n")
        n_products, n_dividers, costs_problems = get_hard_problems()
        for i in range(len(n_products)):
            print(f"Testing hard problem {i+1}")
            problem = (n_products[i], n_dividers[i], costs_problems[i])
            test_problem(problem)

    # Test random problems
    if TEST_RANDOM:
        print("Testing random problems\n")
        for i in range(100):
            print(f"Testing random problem {i+1}")
            problem = get_random_problem(20, force_fewer_dividers=True)
            test_problem(problem)

    # Print results
    if VERIFY_BRUTEFORCE:
        print(f"Tested {n_problems} problems")
        print(f"Correct: {n_correct}")
        print("")