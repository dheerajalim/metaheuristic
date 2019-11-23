"""
Author: Dheeraj Alimchandani

Date : 13-11-2019

File : GWSAT.py

Usage : GWSAT Algorithm
"""

import random
random.seed(2)
from preprocessing import CnfPreprocess
from GSAT import *


class GWSAT:
    def __init__(self):
        self.clause_external = []
        self.clause_list_or = []
        self.clause_list_and = []
        self.sat_variables = []

    def generate_solution(self,preprocess):
        self.sol_list_init = []
        sol_list = [i for i in range(1, preprocess.variable_number + 1)]
        for solution in range(0, len(sol_list)):
            if random.random() < 0.5:
                sol_list[solution] = -1 * sol_list[solution]
        self.sol_list_init = sol_list # Creating a copy of generated sol list before changing it to boolean
        '''Converting the sol_list to truth values'''
        sol_list = [False if var < 0 else True for var in sol_list]
        return sol_list

    def clause_satisfation(self, sol_list, cnf_formula, satcheck):
        """
        The function is responsible to generate the truth values in the clause list based on the solution list
        """
        self.clause_external = []
        for clause in cnf_formula:
            clause_internal = []
            for variable in clause:
                if variable > 0:  # Checking for the True Values
                    clause_internal.append(
                        sol_list[variable - 1])  # Checking the truth value at the index in solution file
                else:  # Checking for the negation values
                    variable_pos = variable * -1
                    clause_internal.append(not (sol_list[variable_pos - 1]))

            self.clause_external.append(clause_internal)
        # print(self.clause_external)
        self.clause_list_or = [any(clause) for clause in self.clause_external]  # Doing OR of Variables
        if not satcheck:
            return self.clause_list_or

        self.clause_list_and = all(self.clause_list_or)  # Doing AND of Clauses
        if satcheck:
            return self.clause_list_and

    def gwsat_solution(self, cnf_formula, max_tries, max_flips, wp, preprocess):

        for try_sol in range(0, max_tries):

            initial_solution = self.generate_solution(preprocess)  # Here we will generate the random solution in the form of Booleans
            # print('Initial Solution :', initial_solution)

            for flip in range(0, max_flips):

                r = random.random()
                # r = 0.1

                if self.clause_satisfation(initial_solution, cnf_formula, satcheck = True):      # Here we will be returned with the and of all clauses
                    ''' Generating the solution by changing the booleans to actual variable '''
                    final_sol_list = [i for i in range(1, preprocess.variable_number + 1)]
                    for item in range(0, len(initial_solution)):
                        if initial_solution[item] is False:
                            final_sol_list[item] = final_sol_list[item] * -1
                    self.sat_variables = final_sol_list
                    return f'Solution is {final_sol_list} generated in {try_sol+1} tries and {max_flips+1} flips'

                else:
                    all_index_unsat_clauses = []
                    cnf_formula_unsat = []

                    # List of all the clauses after performing OR operation on each
                    all_clauses = self.clause_satisfation(initial_solution, cnf_formula, satcheck=False)

                    for index, value in enumerate(all_clauses):
                        if not value:
                            all_index_unsat_clauses.append(index)  # Index of Unsat clauses

                    # Now we will find all the clauses which are unsatisfied
                    for clause_index in all_index_unsat_clauses:
                        cnf_formula_unsat.append(cnf_formula[clause_index])  # List of UNSAT clauses

                    if r < wp:
                        # getting a flat list of all variables in the unsat clauses
                        flat_unsatisified_clauses = [item for sublist in cnf_formula_unsat for item in sublist]
                        # getting all the unique variables in the unsat clauses
                        unique_unsat_variables = set(flat_unsatisified_clauses)

                        random_walk_var = random.choice(list(unique_unsat_variables))

                        flipped_value_index = abs(random_walk_var) - 1
                        # print(flipped_value_index)

                    else:
                        sol_list_init = []
                        # Generating the variable solution list from the boolean list
                        for index, var in enumerate(initial_solution):
                            if not var:
                                sol_list_init.append(-1 * (index + 1))
                            else:
                                sol_list_init.append((index + 1))

                        # print(all_clauses)
                        flipped_value_index = GSAT().gsat_solution(cnf_formula, sol_list_init, all_clauses, cnf_formula_unsat)

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
    result = gwsat.gwsat_solution(cnf_formula, max_tries, max_flips,wp, preprocess)
    print(result)
    gwsat.solution_txt()

