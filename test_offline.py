### IMPORTS ###

# Standard library imports
import time
import itertools

# Self-defined imports
from algorithm import *
from example_problems import *


### TEST PARAMETERS ###

# Parameters for testing random problems of a given size
TEST_RANDOM = False
N_PROBLEMS_RANDOM = 1000
N_PRODUCTS_RANDOM = 5

# Parameters for testing all problems of a given size
TEST_ALL = True
N_PRODUCTS_ALL = 8

# Verification and verbosity parameters
VERIFY_BRUTEFORCE = True
VERBOSE = False


### CORRECTNESS COUNTERS ###

n_problems, n_correct = 0, 0


### OFFLINE TESTING ###

def test_algorithm(problem, algorithm, algorithm_name, verbose=False):
    """ Solve the given problem using the given algorithm """
    # Extract problem parameters
    n_products, n_dividers, costs = problem
    # Set start time
    start_time = time.time()
    # Execute algorithm
    answer = algorithm(n_products, n_dividers, costs)
    # Compute end time
    end_time = time.time()
    # If VERBOSE, print the result and how long it took to compute
    if verbose:
        print(f"{algorithm_name}: {answer} ({end_time-start_time:.3f} seconds)")
    # Return the answer
    return answer


def test_problem(problem):
    """ Test a given problem """
    # Increment the problem counter
    global n_problems
    n_problems += 1
    # If the answer needs to be verified, run the brute-force algorithm to get the correct solution
    if VERIFY_BRUTEFORCE:
        solution = test_algorithm(problem, brute_force, "Brute Force")
    # Get the answer from the "semi-greedy" algorithm
    answer = test_algorithm(problem, semi_greedy, "Semi-greedy")
    # If The answer needs to be verified:
    if VERIFY_BRUTEFORCE:
        # Check if the answer was correct
        correct = answer == solution[0]
        # Print whether the answer was correct
        print("CORRECT" if correct else "INCORRECT")
        # Increment the correctness counter
        global n_correct
        n_correct += 1 if correct else 0
        # If VERBOSE, print the problem if the answer was incorrect
        if not correct and VERBOSE:
            print(problem)
        # If VERBOSE, go to a new line
        if VERBOSE:
            print("")
        # Return whether the answer was correct
        return correct
    # Otherwise, if VERBOSE, go to a new line
    elif VERBOSE:
        print("") 


def test_problems_list(problems, type):
    """ Test all problems in a list of problems """
    # Print the type of problem list being tested
    print(f"Testing {type} problems\n")
    # Initialize a list of mistakes
    mistakes = []
    # Loop through the list of problems
    for i, problem in enumerate(problems):
        # Print the problem being tested
        print(f"Testing problem {i+1}: {problem} ", end="" if VERIFY_BRUTEFORCE else "\n")
        # If the answer needs to be verified, test the problem and add it to the list of mistakes if the answer was not correct
        if VERIFY_BRUTEFORCE:
            correct = test_problem(problem)
            if not correct:
                mistakes.append(problem)
        # Otherwise, simply test the problem
        else:
            test_problem(problem)
    # If the answers were verified, print the number of mistakes made as well as the list of mistakes
    if VERIFY_BRUTEFORCE:
        print(f"\nMade {len(mistakes)} mistakes: {mistakes}")


### RUNNING THE FILE ###

if __name__ == "__main__":

    # Test random problems
    if TEST_RANDOM:
        problems = [get_random_problem(N_PRODUCTS_RANDOM, force_fewer_dividers=True) for i in range(N_PROBLEMS_RANDOM)]
        test_problems_list(problems, "random")

    # Test all possible combinations
    if TEST_ALL:
        problems = get_all_problems(N_PRODUCTS_ALL)
        test_problems_list(problems, "all")

    # Print results if answers were verified
    if VERIFY_BRUTEFORCE:
        print(f"\nTested {n_problems} problems")
        print(f"Correct: {n_correct}")
        print("")