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


class BruteForce(Algorithm):
    """
    Brute force algorithm that tries all possible combinations given the number of dividers
    Always returns correct answer but has complexity 2^n (because it creates a binary tree if n_dividers=0)
    """
    def __init__(self):
        super(BruteForce, self).__init__()

    def run(self, n_products, n_dividers, costs):
        start_checkout = [costs.pop(0)]
        n_divs_used = 0
        # Get all possible ways to order products
        all_checkouts = self._brute_force_helper(start_checkout, costs, n_divs_used, n_dividers)
        # Round all costs to 5
        rounded_checkouts = [[u.round_to_5(cost) for cost in checkout] for checkout in all_checkouts]
        # Compute the sum of all checkouts and return the minimum value
        cost_checkouts = [sum(checkout) for checkout in rounded_checkouts]
        return min(cost_checkouts)

    def _brute_force_helper(self, checkout, costs, n_divs_used, n_dividers):
        """
        Recursive function that computes all possible checkouts of products by either placing or not placing a divider
        (given the n_dividers)
        """
        all_checkouts = []
        # Base case: if we have had all products, return the current checkout
        if len(costs) == 0:
            return [checkout]
        # Base case: if we have used all our dividers, add all remaining products to current product group
        elif n_divs_used == n_dividers:
            checkout[-1] += sum(costs)
            return [checkout]
        # Recursive case: do and do not place divider
        else:
            # Get the new cost (and remove it from the costs list)
            cur_cost = costs.pop(0)

            # Case 1: add the product to the current product group (place no divider)
            checkout_add = checkout.copy()
            checkout_add[-1] += cur_cost
            children_add = self._brute_force_helper(checkout_add, costs.copy(), n_divs_used, n_dividers)
            all_checkouts.extend(children_add)

            # Case 2: start new product group (by placing divider)
            checkout_append = checkout.copy()
            checkout_append.append(cur_cost)
            children_append = self._brute_force_helper(checkout_append, costs.copy(), n_divs_used + 1, n_dividers)
            all_checkouts.extend(children_append)

            return all_checkouts
