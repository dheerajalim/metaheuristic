"""
Author: Dheeraj Alimchandani

Date : 13-11-2019

File : WalkSAT.py

Usage : WalkSAT Algorithm
"""

import random
from time import time
import queue
from preprocessing import CnfPreprocess
from utils import Utils as ut

random.seed(2)


class WalkSAT:

    def __init__(self):
        self.sat_variables = []

    def zero_negative_gain(self,negative_gain,unsat_clause_selection):

        zero_negative_gain = [index for index, zero in enumerate(negative_gain) if zero == 0]

        if len(zero_negative_gain) > 1:  # If more than one -ve gain with 0
            flipped_value_var = random.choices(zero_negative_gain)
            flipped_value_index = abs(unsat_clause_selection[flipped_value_var[0]]) - 1
        else:
            flipped_value_index = abs(unsat_clause_selection[zero_negative_gain[0]]) - 1

        return flipped_value_index

    def min_negative_gain(self, negative_gain, unsat_clause_selection):

        min_value = min(negative_gain)
        min_negative_gain = [index for index, min in enumerate(negative_gain) if min == min_value]
        if len(min_negative_gain) > 1:  # If more than one min. -ve gain (breaking tie)
            flipped_value_var = random.choices(min_negative_gain)
            flipped_value_index = abs(unsat_clause_selection[flipped_value_var[0]]) - 1
        else:
            flipped_value_index = abs(unsat_clause_selection[min_negative_gain[0]]) - 1

        return flipped_value_index


    def walksat_solution(self, cnf_formula, max_tries, max_flips, wp, tl, preprocess):

        for try_sol in range(0, max_tries):
            tabu = queue.Queue(maxsize=tl)  # Initializing the tabu queue
            # Here we will generate the random solution in the form of Booleans
            initial_solution = ut.generate_solution(preprocess)

            for flip in range(0, max_flips):
                # Here we will be returned with the and of all clauses
                if ut.clause_satisfation(initial_solution, cnf_formula, satcheck=True):
                    ''' Generating the solution by changing the booleans to actual variable '''
                    final_sol_list = ut.final_solution(initial_solution, preprocess, try_sol, flip)
                    self.sat_variables = final_sol_list
                    return f'Solution is {final_sol_list} generated in {try_sol + 1} tries and {flip + 1} flips'

                else:
                    # sol_list_init = []
                    index_selected_unsat_clause = []

                    '''Generating the variable solution list from the boolean list'''
                    sol_list_init = ut().variable_sol_list(initial_solution)

                    # List of all the clauses after performing OR operation on each
                    all_clauses = ut.clause_satisfation(initial_solution, cnf_formula, satcheck=False)

                    cnf_formula_unsat = ut().unsat_clauses(all_clauses, cnf_formula) # All unsat clauses
                    cnf_formula_sat = ut().sat_clauses(all_clauses, cnf_formula)    # All SAT clauses

                    # Selecting UNSAT clause randomly
                    unsat_clause_selection = random.choice(cnf_formula_unsat)

                    '''CHECKING THE TABU LIST, if all the variables in selected unsat clauses are on the tabu list'''
                    tabu_list = list(tabu.queue)

                    # Creating the selected usat clause variable list (not literal)
                    abs_unsat_clause_selection = [abs(var) for var in unsat_clause_selection]

                    # if all the variables are in tabu list then
                    if set(abs_unsat_clause_selection).issubset(set(tabu_list)):
                        continue

                    '''We will check for each variale if that variable in UNSAT clause exists in tabu list
                        If yes : The remove that variable from tabu list.
                        It is a preprocessed step to reduce operation cost of checking tabu list after the var 
                        selection
                    '''
                    for index,var in enumerate(abs_unsat_clause_selection):
                        if var in tabu.queue:
                            index_selected_unsat_clause.append(index)

                    # Now lets remove the variables from selected unsat clause which are in tabu list
                    unsat_clause_selection = [i for j,i in enumerate(unsat_clause_selection) if j not in index_selected_unsat_clause]

                    # If only single variable is present in the unsat clause after tabu check, then just flip that
                    if len(unsat_clause_selection) == 1:
                        flipped_value_index = abs(unsat_clause_selection[0]) - 1

                    else:
                        # Computing negative gain of the variables in selected unsat clauses
                        negative_gain = ut.negative_gain(sol_list_init, cnf_formula_sat, unsat_clause_selection)

                        if 0 in negative_gain:
                            '''Checking for the variables with negative gain of 0'''
                            flipped_value_index = self.zero_negative_gain(negative_gain, unsat_clause_selection)

                        else:
                            r = random.random()
                            if r < wp:
                                '''getting a random variable in the selected unsat clauses'''
                                flipped_value_var = random.choice(unsat_clause_selection)
                                flipped_value_index = abs(flipped_value_var) - 1

                            else:
                                '''Selecting the variable with minimum negative gain'''
                                flipped_value_index = self.min_negative_gain(negative_gain, unsat_clause_selection)

                    '''Manipulating the tabu list'''
                    if tabu.full():
                        tabu.get()
                    tabu.put(flipped_value_index+1)

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
    tl = 5
    cnf_instance = 'Lab-data/Lab-data/Inst/uf20-06.cnf'
    preprocess = CnfPreprocess(cnf_instance)
    cnf_formula = preprocess.filter_cnf_instance()
    walksat = WalkSAT()
    start = time()
    result = walksat.walksat_solution(cnf_formula, max_tries, max_flips, wp, tl, preprocess)
    print(f'The execution took {round(time() - start, 3)} seconds')
    print(result)
    walksat.solution_txt()
