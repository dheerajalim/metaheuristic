"""
Author: Dheeraj Alimchandani

Date : 13-11-2019

File : GWSAT.py

Usage : GWSAT Algorithm
"""

import random
from time import time
from preprocessing import CnfPreprocess
from GSAT import GSAT
from utils import Utils as ut

random.seed(2)


class GWSAT:

    def __init__(self):
        self.sat_variables = []

    def gwsat_solution(self, cnf_formula, max_tries, max_flips, wp, preprocess):

        for try_sol in range(0, max_tries):

            # Here we will generate the random solution in the form of Booleans
            initial_solution = ut.generate_solution(preprocess)

            for flip in range(0, max_flips):
                r = random.random()
                # Here we will be returned with the and of all clauses
                if ut.clause_satisfation(initial_solution, cnf_formula,satcheck=True):
                    ''' Generating the solution by changing the booleans to actual variable '''
                    final_sol_list = ut.final_solution(initial_solution, preprocess, try_sol, flip)
                    self.sat_variables = final_sol_list
                    return f'Solution is {final_sol_list} generated in {try_sol + 1} tries and {flip + 1} flips'

                else:
                    # List of all the clauses after performing OR operation on each
                    all_clauses = ut.clause_satisfation(initial_solution, cnf_formula, satcheck=False)
                    cnf_formula_unsat = ut().unsat_clauses(all_clauses, cnf_formula)  # All unsat clauses

                    if r < wp:
                        # getting a flat list of all variables in the unsat clauses
                        flat_unsatisified_clauses = [item for sublist in cnf_formula_unsat for item in sublist]
                        # getting all the unique variables in the unsat clauses
                        unique_unsat_variables = set(flat_unsatisified_clauses)
                        # Randomly selecting variable from the list
                        random_walk_var = random.choice(list(unique_unsat_variables))
                        flipped_value_index = abs(random_walk_var) - 1

                    else:
                        sol_list_init = []
                        # Generating the variable solution list from the boolean list
                        for index, var in enumerate(initial_solution):
                            if not var:
                                sol_list_init.append(-1 * (index + 1))
                            else:
                                sol_list_init.append((index + 1))

                        flipped_value_index = GSAT().gsat_solution(cnf_formula, sol_list_init, all_clauses,
                                                                   cnf_formula_unsat)

                    '''Flipping the initial_solution variable'''
                    initial_solution[flipped_value_index] = not (initial_solution[flipped_value_index])

        return 'No Solution'

    def solution_txt(self):
        with open('sol_gwsat.txt', 'w') as sat_sol:
            sat_sol.write('c Solution generated using GWSAT \n')
            sat_sol.write('v')
            for variables in self.sat_variables:
                if variables % 11 == 0:
                    sat_sol.write('\n')
                    sat_sol.write('v')
                sat_sol.write(f' {str(variables)} ')


if __name__ == '__main__':
    max_tries = 10
    max_flips = 100
    wp = 0.4
    cnf_instance = 'Lab-data/Lab-data/Inst/uf20-06.cnf'
    preprocess = CnfPreprocess(cnf_instance)
    cnf_formula = preprocess.filter_cnf_instance()
    gwsat = GWSAT()
    start = time()
    result = gwsat.gwsat_solution(cnf_formula, max_tries, max_flips, wp, preprocess)
    print(f'The execution took {round(time() - start, 3)} seconds')
    print(result)
    gwsat.solution_txt()
