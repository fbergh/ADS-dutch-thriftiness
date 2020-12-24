import utils as u
import math


class Algorithm(object):
    """ Base class for algorithms """

    def run(self, n_products, n_dividers, costs):
        # If we have no dividers, we can sum the costs and round them
        if n_dividers == 0:
            return u.round_to_5(sum(costs))
        return None


class BruteForce(Algorithm):
    """
    Brute force algorithm that tries all possible combinations given the number of dividers
    Always returns correct answer but has complexity 2^n (because it creates a binary tree if n_dividers=0)
    """

    def __init__(self):
        super(BruteForce, self).__init__()
        self.min_checkout = math.inf

    def run(self, n_products, n_dividers, costs):
        print("Brute force")
        # Run base cases
        base_case_cost = super().run(n_products, n_dividers, costs)
        if base_case_cost is not None:
            return base_case_cost
        else:
            # Set initial minimum to checkout with no dividers
            self.min_checkout = u.round_to_5(sum(costs))

            # Get all values for which holds value % 5 = 0
            # The order of these values doesn't matter (because they don't have to be rounded) and can be added
            # in the end
            mod_5_values = u.get_mod_5_values(costs)
            print("Mod 5 values: ", mod_5_values)

            start_checkout = [costs.pop(0)]
            n_divs_used = 0
            # Get all possible ways to order products
            all_checkouts = self._brute_force_helper(start_checkout, costs, n_divs_used, n_dividers)
            print("All checkouts: ", all_checkouts)
            # Compute total (rounded) cost of checkouts (add mod 5 values)
            cost_checkouts = [u.cost_of_checkout(checkout) + sum(mod_5_values) for checkout in all_checkouts]
            print("Cost of all checkouts: ", cost_checkouts)
            return min(cost_checkouts)

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

    def reset(self):
        self.min_checkout = math.inf


class CheckoutCutting(Algorithm):
    """
    This algorithm is inspired by the rod cutting algorithm. We look at all possible positions to place a divider.
    On the most optimal place, if it exists, we place one and then repeat the same procedure for the worst side.
    If it does not exist, we are done with that side.

    NOTE: the algorithm is only partially correct now (seems to be about 80-90% correct)

    Algorithm is O(n*k) (I think), where n=#products and k=#dividers
    """
    def __init__(self):
        super(CheckoutCutting, self).__init__()

    def run(self, n_products, n_dividers, costs):
        # Run base cases
        base_case_cost = super().run(n_products, n_dividers, costs)
        if base_case_cost is not None:
            return base_case_cost
        else:
            return self.checkout_cutting(n_dividers, costs)

    def checkout_cutting(self, n_dividers, costs):
        print(costs)
        if len(costs) == 1 or n_dividers == 0:
            return u.cost_of_checkout([costs])
        else:
            # Set best_checkout to checkout with no dividers to determine if it's even worth placing dividers
            best_checkout = [costs]
            # Bad initial values for gain
            best_gain = (-math.inf, -math.inf)
            # For every position where we can place the divider (so not 0)
            for div_pos in range(1, len(costs)):
                cur_checkout = [u.to_list(costs[:div_pos]), u.to_list(costs[div_pos:])]
                cur_gain = u.gain_of_checkout(cur_checkout)
                if self.is_cur_checkout_better(best_checkout, best_gain, cur_checkout, cur_gain):
                    best_checkout = cur_checkout
                    best_gain = cur_gain
                if best_gain == (2, 2) and n_dividers == 1:
                    return u.cost_of_checkout(best_checkout)

            # If we have used no divider, stop recursing and return sum
            if best_gain == (-math.inf, -math.inf):
                return u.cost_of_checkout(best_checkout)
            # If we have used one, keep best side in tact and recurse
            else:
                best_idx = self.get_idx_best_side(best_gain, best_checkout)
                best_side, worst_side = best_checkout[best_idx], best_checkout[not best_idx]
                # NOTE: only recurse on bad side? Probably not...
                # If we want to recurse on best side too, dividers should be a class attribute, but how do we decide
                # which side gets to use how many dividers?
                return u.round_to_5(sum(best_side)) + self.checkout_cutting(n_dividers - 1, worst_side)

    def is_cur_checkout_better(self, best_checkout, best_gain, cur_checkout, cur_gain):
        # NOTE: the algorithm is partially correct, some of these cases might therefore be incorrect...

        # If the current cost is greater than the best checkout, it sucks
        if u.cost_of_checkout(cur_checkout) > u.cost_of_checkout(best_checkout):
            return False
        # If the current cost is smaller than the best checkout, it's great
        elif u.cost_of_checkout(cur_checkout) < u.cost_of_checkout(best_checkout):
            return True
        # If the maximal gain value of the current checkout is better than that of the best checkout, it's great
        # E.g. given current (2,-2) and best (1,-1), then 2 > 1, so current > best
        if max(cur_gain) > max(best_gain):
            return True
        # If the gain values of best and current are equal, we check if the same gain is achieved with fewer values in current
        # If so, it's great
        is_gain_equal = sorted(best_gain) == sorted(cur_gain)
        if is_gain_equal:
            max_idx_c = cur_gain.index(max(cur_gain))
            max_idx_b = best_gain.index(max(best_gain))
            return len(best_checkout[max_idx_b]) > len(cur_checkout[max_idx_c])
        # If none of the above hold, it sucks
        return False

    def get_idx_best_side(self, best_gain, best_checkout):
        # If index 1 is the best this will return True (i.e. 1), else False (i.e. 0)
        return best_gain[1] > best_gain[0] \
               or best_gain[1] == best_gain[0] and len(best_checkout[1]) < len(best_checkout[0])