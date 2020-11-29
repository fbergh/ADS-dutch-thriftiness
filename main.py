import input_output as io
from algorithm import NoDividers, DumbSinglePass


def test_server():
    n_products, n_dividers, costs = io.get_values_from_input()
    algorithm = DumbSinglePass()
    min_sum = algorithm.run(n_products, n_dividers, costs)
    io.eprint(min_sum)
    io.send(min_sum)


if __name__ == '__main__':
    test_server()
