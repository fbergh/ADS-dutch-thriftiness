import utils as u
import math


class Algorithm(object):
    """ Base class for algorithms """

    def run(self, n_products, n_dividers, costs):
        # If we have no dividers, we can sum the costs and round them
        if n_dividers == 0:
            return u.round_to_5(sum(costs))
        return None


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
        self.min_checkout = math.inf

    def run(self, n_products, n_dividers, costs):
        # Run base cases
        base_cost = super().run(n_products, n_dividers, costs)
        if base_cost is not None:
            return base_cost
        else:
            # Set initial minimum to checkout with no dividers
            self.min_checkout = u.round_to_5(sum(costs))

            # Get all values for which holds value % 5 = 0
            # The order of these values doesn't matter (because they don't have to be rounded) and can be added
            # in the end
            mod_5_values = self.get_mod_5_values(n_products, costs)
            print(mod_5_values)

            start_checkout = [costs.pop(0)]
            n_divs_used = 0
            # Get all possible ways to order products
            all_checkouts = self._brute_force_helper(start_checkout, costs, n_divs_used, n_dividers)
            print(all_checkouts)
            # Compute total (rounded) cost of checkouts (add mod 5 values)
            cost_checkouts = [u.cost_of_checkout(checkout) + sum(mod_5_values) for checkout in all_checkouts]
            print(cost_checkouts)
            return min(cost_checkouts)

    def get_mod_5_values(self, n_products, costs):
        mod_5_values = []
        for i in reversed(range(n_products)):
            if costs[i] % 5 == 0:
                mod_5_values.append(costs.pop(i))
        return mod_5_values

    def _brute_force_helper(self, checkout, costs, n_divs_used, n_dividers):
        """
        Recursive function that computes all possible checkouts of products by either placing or not placing a divider
        (given the n_dividers)
        """
        all_checkouts = []
        # Base case: if we have had all products, return the current checkout
        if len(costs) == 0:
            # Set new minimum checkout for pruning
            if u.cost_of_checkout(checkout) < self.min_checkout:
                self.min_checkout = u.cost_of_checkout(checkout)
            return [checkout]
        # Base case: if we have used all our dividers, add all remaining products to current product group
        elif n_divs_used == n_dividers:
            checkout[-1] += sum(costs)
            # Set new minimum checkout for pruning
            if u.cost_of_checkout(checkout) < self.min_checkout:
                self.min_checkout = u.cost_of_checkout(checkout)
            return [checkout]
        # Recursive case: do and do not place divider
        else:
            # If the cost of the current checkout is equal or greater to the current minimum, prune this branch
            if u.cost_of_checkout(checkout) >= self.min_checkout:
                return []

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
