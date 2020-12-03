import input_output as io
import utils as u


class Algorithm(object):
    """ Base class for algorithms """
    def run(self, n_products, n_dividers, costs):
        # If we have no dividers, we can sum the costs and round them
        if n_dividers == 0:
            return u.round_to_5(sum(costs))
        # If there are n_products-1 dividers, we round each cost individually and then sum the costs
        elif n_dividers == n_products - 1:
            costs = [u.round_to_5(c) for c in costs]
            return sum(costs)
        return None


class NoDividers(Algorithm):
    def __init__(self):
        super(NoDividers, self).__init__()

    def run(self, n_products, n_dividers, costs):
        io.eprint("Using no dividers")
        return sum(costs)


class DumbSinglePass(Algorithm):
    """
    Sequentially adds costs that do not round up (so ending on 0, 1, 2, 5, 6, 7) to one group
    If a cost does round up (ending on 3, 4, 8, 9), place a divider and start the next product group
    If there are no more dividers left, simply sum the remaining products
    In the end returns sum of all product groups
    """
    def __init__(self):
        super(DumbSinglePass, self).__init__()

    def run(self, n_products, n_dividers, costs):
        # Run base cases
        base_cost = super().run(n_products, n_dividers, costs)
        if base_cost is not None:
            return base_cost

        cost_of_group = -1
        costs_of_groups = []
        for i, c in enumerate(costs):
            # If we have used all dividers, sum remaining products
            if n_dividers == 0:
                sum_remaining_prods = u.round_to_5(cost_of_group + sum(costs[i:]))
                costs_of_groups.append(sum_remaining_prods)
                break
            # If adding a the product reduces our cost, add it
            if u.do_add_product(c, cost_of_group):
                if cost_of_group == -1:
                    cost_of_group = 0
                cost_of_group += c
            # If not, place a divider and start again from the current product
            else:
                costs_of_groups.append(u.round_to_5(cost_of_group))
                cost_of_group = c
                n_dividers -= 1
        # Return the sum of all groups of products, separated by dividers
        return sum(costs_of_groups)