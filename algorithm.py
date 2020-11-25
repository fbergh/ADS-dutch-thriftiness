import input_output as io

class Algorithm(object):
    """ Base class for algorithms """
    def run(self, n_products, n_dividers, costs):
        raise NotImplementedError


class NoDividers(Algorithm):
    def __init__(self):
        super(NoDividers, self).__init__()

    def run(self, n_products, n_dividers, costs):
        io.eprint("Using no dividers")
        io.send(sum(costs))
