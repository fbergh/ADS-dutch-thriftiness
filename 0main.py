### IMPORTS ###

# Self-defined imports
import input_output as io
from algorithm import simple_or_greedy


### ONLINE TESTING ###

def test_server():
    """ Solve a problem retrieved from the server """
    n_products, n_dividers, costs = io.get_values_from_input()
    answer = simple_or_greedy(n_products, n_dividers, costs)
    io.send(answer)


### RUNNING THE FILE ###

if __name__ == '__main__':
    test_server()