"""
Author: Dheeraj Alimchandani

File : GSAT.py

Usage : GSAT solution
"""

import random
from utils import Utils as ut


class GSAT:

    def gsat_solution(self, cnf_formula, sol_list_init, all_clauses, cnf_formula_unsat):

        positive_gain = ut.positive_gain(sol_list_init, cnf_formula_unsat)

        cnf_formula_sat = ut().sat_clauses(all_clauses, cnf_formula)  # All SAT clauses

        # Now we wil claculate the negative gain
        negative_gain = ut.negative_gain(sol_list_init, cnf_formula_sat)

        # Finding the Net Gain value for each variable
        net_gain = [x1 - x2 for (x1, x2) in zip(positive_gain, negative_gain)]

        # getting the maximum netgain
        max_netgain = max(net_gain)

        # Getting the indexes of the maximum net gain value
        max_netgain_list = [i for i, x in enumerate(net_gain) if x == max_netgain]

        # To choose randomly the maximum net gain variable if more than one max netgain values presetn
        if len(max_netgain_list) > 1:
            net_gain_index = random.choice(max_netgain_list)
        else:
            net_gain_index = max_netgain_list[0]

        flipped_value_index = net_gain_index
        return flipped_value_index
