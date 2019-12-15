"""
Author: Dheeraj Alimchandani

File : Alimchandani_182505_WalkSAT.py

Usage : WalkSAT Algorithm
"""

import random
from time import time
import queue
from preprocessing import CnfPreprocess
from utils import Utils as ut
import sys

random.seed(2)


class WalkSAT:

    def __init__(self, cut_off_time):
        self.sat_variables = []
        self.cutoff_time = cut_off_time
        self.steps = 0

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
        self.steps = 0
        start_test_time = time()  # To capture the algorithm run starting time
        end_test_time = 0 # To capture the algorithm run time in order to compare with cutoff time
        for try_sol in range(0, max_tries):
            # tabu = queue.Queue(maxsize=tl)  # Initializing the tabu queue
            tabu = {j: 0 for j in [i for i in range(1, preprocess.variable_number + 1)]}  # Initializing the tabu queue

            # Here we will generate the random solution in the form of Booleans
            initial_solution = ut.generate_solution(preprocess)

            for flip in range(0, max_flips):
                self.steps = self.steps + 1

                # Condition to check if the cutoff time is encountered
                if end_test_time > self.cutoff_time:
                    # print(f' Execution Time : {end_test_time} secs to find the solution surpassed cutoff time '
                    #       f'of {self.cutoff_time} seconds ')
                    return 'Cutoff Time'

                # Here we will be returned with the and of all clauses
                if ut.clause_satisfation(initial_solution, cnf_formula, satcheck=True):
                    ''' Generating the solution by changing the booleans to actual variable '''
                    final_sol_list = ut.final_solution(initial_solution, preprocess, try_sol, flip)
                    self.sat_variables = final_sol_list
                    return f'Solution is {final_sol_list} generated in {try_sol} restarts with {flip + 1} flips'

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
                    # tabu_list = list(tabu.queue)

                    # Creating the selected unsat clause variable list (not literal)
                    abs_unsat_clause_selection = [abs(var) for var in unsat_clause_selection]

                    # if all the variables are in tabu list then
                    # if set(abs_unsat_clause_selection).issubset(set(tabu_list)):
                    #     continue

                    # if all the variables are in tabu list then reiterating
                    for var in abs_unsat_clause_selection:
                        if tabu[var] > self.steps:
                            reiterate = True
                        else:
                            reiterate = False
                            break

                    if reiterate:
                        continue

                    '''We will check for each variable if that variable in UNSAT clause exists in tabu list
                        It is a preprocessed step to reduce operation cost of checking tabu list after the var 
                        selection
                    '''

                    # for index,var in enumerate(abs_unsat_clause_selection):
                    #     if var in tabu.queue:
                    #         index_selected_unsat_clause.append(index)

                    for index, var in enumerate(abs_unsat_clause_selection):
                        if tabu[var] > self.steps:
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
                    # if tabu.full():
                    #     tabu.get()
                    # tabu.put(flipped_value_index+1)
                    tabu[flipped_value_index+1] = self.steps + tl

                    '''Flipping the initial_solution variable'''
                    initial_solution[flipped_value_index] = not (initial_solution[flipped_value_index])

                end_test_time = time() - start_test_time  # Calculating the execution time to find the solution

        return 'No Solution'

    def solution_txt(self, filename):

        with open(filename, 'w') as sat_sol:
            sat_sol.write('c Solution generated using WalkSAT \n')
            sat_sol.write('v')
            for variables in self.sat_variables:
                if variables % 11 == 0:
                    sat_sol.write('\n')
                    sat_sol.write('v')
                sat_sol.write(f' {str(variables)} ')


def execution_walksat(walksat, executions):

    """
    :param walksat:  Object of the WalkSAT
    :param executions:  Total number of executions
    :return: Sorted Execution Time list , sorted execution steps list
    """

    time_list = []
    steps_list = []
    for i in range(1, executions + 1):
        print('For the Execution : ', i)
        start = time()
        result = walksat.walksat_solution(cnf_formula, max_tries, max_flips, wp, tl, preprocess)
        end = round(time() - start, 3)

        if result != 'Cutoff Time' and result != 'No Solution':
            time_list.append(end)
            steps_list.append(walksat.steps)

        print(f'The execution took {end} seconds (Cutoff Time: {walksat.cutoff_time} seconds)')
        print(result)

    return sorted(time_list), sorted(steps_list)


if __name__ == '__main__':
    executions = int(sys.argv[2])  # No. of Executions
    max_tries = int(sys.argv[3])  # Restarts
    max_flips = int(sys.argv[4])  # Iterations per restart
    wp = float(sys.argv[5])    # Random Walk Probability
    tl = int(sys.argv[6])  # Tabu length
    cutoff_time = float(sys.argv[7])  # cut off time in seconds
    cnf_instance = sys.argv[1]    # cnf file instance

    # Validating the input from the user
    ut.input_sanitization(executions, max_tries, max_flips, wp, cutoff_time, cnf_instance, tl)

    preprocess = CnfPreprocess(cnf_instance) # Pre processing the cnf instance
    cnf_formula = preprocess.filter_cnf_instance()  # Filtering the cnf instances clauses
    walksat = WalkSAT(cutoff_time)

    # Generating the results based on given number of executions
    cputime_sorted, steptime_sorted = execution_walksat(walksat, executions)

    # Generating the run-time( CPU time) vs P(solve) graph
    ut.runtime_plot(cputime_sorted, executions,'Run Time(CPU sec)', 'P(solve)','WalkSAT RTD', plot_type='normal')

    # Generating the run-time( Search Steps) vs P(solve) graph
    ut.runtime_plot(steptime_sorted, executions,'Run Time(Search Steps)', 'P(solve)','WalkSAT RTD', plot_type='normal')

    # Generating semi log for the run-time( CPU time) vs P(solve) graph
    ut.runtime_plot(cputime_sorted, executions, 'Run Time(CPU sec)', 'P(solve)', 'WalkSAT RTD Semi log Plot',
                    plot_type='semi_log')

    # Generating semi log graph for run-time( Search Steps) vs P(solve) graph
    ut.runtime_plot(steptime_sorted, executions, 'Run Time(Search Steps)', 'P(solve)', 'WalkSAT RTD Semi log Plot',
                    plot_type='semi_log')

    # Generating log log for the run-time( CPU time) vs P(solve) graph
    ut.runtime_plot(cputime_sorted, executions, 'Run Time(CPU sec)', 'P(solve)', 'WalkSAT RTD log log Plot',
                    plot_type='log_log')

    # Generating log log graph for run-time( Search Steps) vs P(solve) graph
    ut.runtime_plot(steptime_sorted, executions, 'Run Time(Search Steps)', 'P(solve)', 'WalkSAT RTD log log Plot',
                    plot_type='log_log')

    # Generating f rate log log for the run-time( CPU time) vs P(solve) graph
    ut.runtime_plot(cputime_sorted, executions, 'Run Time(CPU sec)', 'P(solve)', 'WalkSAT RTD F rate log log Plot',
                    plot_type='f_rate_log_log')

    # Generating f rate log log graph for run-time( Search Steps) vs P(solve) graph
    ut.runtime_plot(steptime_sorted, executions, 'Run Time(Search Steps)', 'P(solve)', 'WalkSAT RTD F rate log Log Plot',
                    plot_type='f_rate_log_log')

    # To generate the solution text file
    # walksat.solution_txt('walksat_cnf50-01.txt')
