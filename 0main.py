import input_output as io
from algorithm import greedy


def test_server():
    n_products, n_dividers, costs = io.get_values_from_input()
    answer = greedy(n_products, n_dividers, costs)
    io.eprint(answer)
    io.send(answer)


if __name__ == '__main__':
    test_server()