import input_output as io
from algorithm import DumbSinglePass, BruteForce
import random


def test_server():
    n_products, n_dividers, costs = io.get_values_from_input()
    algorithm = BruteForce()
    min_sum = algorithm.run(n_products, n_dividers, costs)
    io.eprint(min_sum)
    io.send(min_sum)


def test_local():
    random.seed(1)
    n_products = 100
    n_dividers = random.randint(0, 25)
    costs = [random.randint(1, 50) for _ in range(n_products)]
    print(costs)
    algorithm = BruteForce()
    min_sum = algorithm.run(n_products, n_dividers, costs)
    print(min_sum)


if __name__ == '__main__':
    test_local()
