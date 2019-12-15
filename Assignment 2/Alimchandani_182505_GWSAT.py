"""
Author: Dheeraj Alimchandani

File : Alimchandani_182505_GWSAT.py

Usage : GWSAT Algorithm
"""

import random
from time import time
from preprocessing import CnfPreprocess
from GSAT import GSAT
from utils import Utils as ut
import sys

random.seed(2)


class GWSAT:

    def __init__(self, cut_off_time):
        self.sat_variables = []
        self.cutoff_time = cut_off_time
        self.steps = 0

    def gwsat_solution(self, cnf_formula, max_tries, max_flips, wp, preprocess):
        self.steps = 0
        start_test_time = time()  # To capture the algorithm run starting time
        end_test_time = 0 # To capture the algorithm run time in order to compare with cutoff time
        for try_sol in range(0, max_tries):

            # Here we will generate the random solution in the form of Booleans
            initial_solution = ut.generate_solution(preprocess)

            for flip in range(0, max_flips):
                self.steps = self.steps + 1     # Keeping a count of the steps

                # Condition to check if the cutoff time is encountered
                if end_test_time > self.cutoff_time:
                    # print(f' Execution Time : {end_test_time} secs to find the solution surpassed cutoff time '
                    #       f'of {self.cutoff_time} seconds ')
                    return 'Cutoff Time'

                r = random.random()
                # Here we will be returned with the 'and' of all clauses
                if ut.clause_satisfation(initial_solution, cnf_formula,satcheck=True):
                    ''' Generating the solution by changing the booleans to actual variable '''
                    final_sol_list = ut.final_solution(initial_solution, preprocess, try_sol, flip)
                    self.sat_variables = final_sol_list
                    return f'Solution is {final_sol_list} generated in {try_sol} restart with {flip + 1} flips'

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

                end_test_time = time() - start_test_time  # Calculating the execution time to find the solution

        return 'No Solution'

    def solution_txt(self, filename):

        with open(filename, 'w') as sat_sol:
            sat_sol.write('c Solution generated using GWSAT \n')
            sat_sol.write('v')
            for variables in self.sat_variables:
                if variables % 11 == 0:
                    sat_sol.write('\n')
                    sat_sol.write('v')
                sat_sol.write(f' {str(variables)} ')


def execution_gwsat(gwsat, executions):
    """

    :param gwsat:  Object of the GWSAT
    :param executions:  Total number of executions
    :return: Sorted Execution Time list , sorted execution steps list
    """

    time_list = []
    steps_list = []
    for i in range(1, executions + 1):
        print('For the Execution : ', i)
        start = time()
        result = gwsat.gwsat_solution(cnf_formula, max_tries, max_flips, wp, preprocess)
        end = round(time() - start, 3)

        if result != 'Cutoff Time' and result != 'No Solution':
            time_list.append(end)
            steps_list.append(gwsat.steps)

        print(f'The execution took {end} seconds (Cutoff Time: {gwsat.cutoff_time} seconds)')
        print(result)

    return sorted(time_list), sorted(steps_list)


if __name__ == '__main__':
    executions = int(sys.argv[2])  # No. of Executions 100
    max_tries = int(sys.argv[3])   # No. of restarts 10
    max_flips = int(sys.argv[4]) # Iterations per restart 1000
    wp = float(sys.argv[5])    # Random Walk Probability 0.4
    cutoff_time = float(sys.argv[6])  # cut off time in seconds 5.0
    cnf_instance = sys.argv[1]      # cnf file instance

    # Validating the input from the user
    ut.input_sanitization(executions, max_tries, max_flips, wp, cutoff_time, cnf_instance)

    preprocess = CnfPreprocess(cnf_instance)  # Pre processing the cnf instance
    cnf_formula = preprocess.filter_cnf_instance()  # Filtering the cnf instances clauses
    gwsat = GWSAT(cutoff_time)

    # Generating the results based on given number of executions
    cputime_sorted, steptime_sorted = execution_gwsat(gwsat, executions)

    # Generating the run-time( CPU time) vs P(solve) graph
    ut.runtime_plot(cputime_sorted, executions,'Run Time(CPU sec)', 'P(solve)','GWSAT RTD', plot_type='normal')

    # Generating the run-time( Search Steps) vs P(solve) graph
    ut.runtime_plot(steptime_sorted, executions,'Run Time(Search Steps)', 'P(solve)','GWSAT RTD', plot_type='normal')

    # Generating semi log for the run-time( CPU time) vs P(solve) graph
    ut.runtime_plot(cputime_sorted, executions, 'Run Time(CPU sec)', 'P(solve)','GWSAT RTD Semi log Plot',
                    plot_type='semi_log')

    # Generating semi log graph for run-time( Search Steps) vs P(solve) graph
    ut.runtime_plot(steptime_sorted, executions, 'Run Time(Search Steps)', 'P(solve)', 'GWSAT RTD Semi Log Plot',
                    plot_type='semi_log')

    # Generating log log for the run-time( CPU time) vs P(solve) graph
    ut.runtime_plot(cputime_sorted, executions, 'Run Time(CPU sec)', 'P(solve)','GWSAT RTD log log Plot',
                    plot_type='log_log')

    # Generating log log graph for run-time( Search Steps) vs P(solve) graph
    ut.runtime_plot(steptime_sorted, executions, 'Run Time(Search Steps)', 'P(solve)', 'GWSAT RTD log Log Plot',
                    plot_type='log_log')

    # Generating f rate log log for the run-time( CPU time) vs P(solve) graph
    ut.runtime_plot(cputime_sorted, executions, 'Run Time(CPU sec)', 'P(solve)','GWSAT RTD F rate log log Plot',
                    plot_type='f_rate_log_log')

    # Generating f rate log log graph for run-time( Search Steps) vs P(solve) graph
    ut.runtime_plot(steptime_sorted, executions, 'Run Time(Search Steps)', 'P(solve)', 'GWSAT RTD F rate log Log Plot',
                    plot_type='f_rate_log_log')

    # To generate the solution text file
    # gwsat.solution_txt('gsat_cnf50-01.txt')
