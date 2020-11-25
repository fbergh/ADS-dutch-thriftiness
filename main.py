import input_output as io
from algorithm import NoDividers


def test_server():
    n_products, n_dividers, costs = io.get_values_from_input()
    algorithm = NoDividers()
    algorithm.run(n_products, n_dividers, costs)


if __name__ == '__main__':
    test_server()
