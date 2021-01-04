### IMPORTS ###

# Standard library imports
import time
import itertools

# Self-defined imports
from algorithm import *
from example_problems import *


### CONSTANTS ###

TEST_SIMPLE = False
TEST_HARD = False

TEST_RANDOM = False
TEST_ALL = True

VERIFY_BRUTEFORCE = True

N_PRODUCTS_ALL = 7

N_PROBLEMS_RANDOM = 100
N_PRODUCTS_RANDOM = 20

VERBOSE = False

### CORRECTNESS COUNTERS ###

n_problems = 0
n_correct = 0


### OFFLINE TESTING ###

def test_algorithm(problem, algorithm, algorithm_name, verbose=False):
    n_products, n_dividers, costs = problem
    start_time = time.time()
    cost = algorithm(n_products, n_dividers, costs)
    end_time = time.time()
    if verbose:
        print(f"{algorithm_name}: {cost} ({end_time-start_time:.3f} seconds)")
    return cost

def test_problem(problem):
    global n_problems
    n_problems += 1
    if VERIFY_BRUTEFORCE:
        solution = test_algorithm(problem, brute_force, "Brute force")
    answer = test_algorithm(problem, greedy, "Greedy")
    if VERIFY_BRUTEFORCE:
        correct = answer == solution[0]
        print("CORRECT" if correct else "INCORRECT")
        global n_correct
        n_correct += 1 if correct else 0
        if not correct and VERBOSE:
            print(problem)
        if VERBOSE:
            print("")
        return correct
    if VERBOSE:
        print("") 

def test_problems_list(problems, name):
    mistakes = []
    print(f"Testing {name} problems\n")
    for i, problem in enumerate(problems):
        print(f"Testing problem {i+1}: {problem} ", end="")
        if VERIFY_BRUTEFORCE:
            correct = test_problem(problem)
            if not correct:
                mistakes.append(problem)
        else:
            test_problem(problem)
    if VERIFY_BRUTEFORCE:
        print(f"\nMade {len(mistakes)} mistakes:")
        print(mistakes)


if __name__ == "__main__":

    # Test simple problems
    if TEST_SIMPLE:
        test_problems_list(get_simple_problems(), "simple")

    # Test hard problems
    if TEST_HARD:
        test_problems_list(get_hard_problems(), "hard")

    # Test random problems
    if TEST_RANDOM:
        problems = [get_random_problem(N_PRODUCTS_RANDOM, force_fewer_dividers=True) for i in range(N_PROBLEMS_RANDOM)]
        test_problems_list(problems, "random")

    # Test all possible combinations
    if TEST_ALL:
        problems = []
        all_sets = itertools.combinations_with_replacement([1,2,3,4], N_PRODUCTS_ALL)
        for s in all_sets:
            all_costs = list(set([costs for costs in itertools.permutations(s)]))
            for costs in all_costs:
                for n_dividers in range(N_PRODUCTS_ALL):
                    problems.append((N_PRODUCTS_ALL, n_dividers, costs))
        test_problems_list(problems, "all")

    # Print results
    if VERIFY_BRUTEFORCE:
        print(f"\nTested {n_problems} problems")
        print(f"Correct: {n_correct}")
        print("")