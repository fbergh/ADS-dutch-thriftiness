import input_output as io
from problem_io import *
from algorithm import BruteForce, CheckoutCutting
import random


def test_server():
    n_products, n_dividers, costs = io.get_values_from_input()
    algorithm = BruteForce()
    min_sum = algorithm.run(n_products, n_dividers, costs)
    io.eprint(min_sum)
    io.send(min_sum)


def test_local(algorithm, n_problems, seed=None, do_sample_problems=False):
    brute = BruteForce()

    if do_sample_problems:
        print("Sample problem 1")
        n_products, n_dividers, costs = data_sample1()
        print(algorithm.run(n_products, n_dividers, costs.copy()) == 755, "\n")

        print("Sample problem 2")
        n_products, n_dividers, costs = data_sample2()
        print(algorithm.run(n_products, n_dividers, costs.copy()) == 0, "\n")

    if seed is not None:
        random.seed(seed)
    else:
        seed = random.random()
        print(seed)
        random.seed(seed)

    correct = []

    for i in range(n_problems):
        print(f"--- Problem {i+1} ---")
        n_products, n_dividers, costs = data_random(20)
        print(n_products, n_dividers, costs, "\n", sep="\n")
        correct_answer = brute.run(n_products, n_dividers, costs.copy())
        brute.reset()
        print()
        answer = algorithm.run(n_products, n_dividers, costs.copy())
        correct.append(correct_answer == answer)
        print(f"\nBrute force: {correct_answer}\nAlgorithm: {answer}\nCorrect: {correct_answer == answer}")

    print(f"\nNumber correct: {sum(correct)}/{n_problems}")


if __name__ == '__main__':
    a = CheckoutCutting()
    test_local(a, 10)#, 0.39701436528658685)
