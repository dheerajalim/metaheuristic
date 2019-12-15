"""
Author: Dheeraj Alimchandani

File : utils.py

Usage : Utility functions
"""

import random
import matplotlib.pyplot as plt
from statistics import mean, median, stdev


class Utils:

    @staticmethod
    def generate_solution(preprocess):
        """
        :param preprocess: Object of CnfPreprocess class
        :return: A list of variables with boolean values
        """
        sol_list = [i for i in range(1, preprocess.variable_number + 1)]
        for solution in range(0, len(sol_list)):
            if random.random() < 0.5:
                sol_list[solution] = -1 * sol_list[solution]
        '''Converting the sol_list to truth values'''
        sol_list = [False if var < 0 else True for var in sol_list]
        return sol_list

    @staticmethod
    def clause_satisfation(sol_list, cnf_formula, satcheck):
        """
        The function is responsible to generate the truth values in the clause list based on the solution list
        """
        clause_external = []
        for clause in cnf_formula:
            clause_internal = []
            for variable in clause:
                if variable > 0:  # Checking for the True Values
                    clause_internal.append(
                        sol_list[variable - 1])  # Checking the truth value at the index in solution file
                else:  # Checking for the negation values
                    variable_pos = variable * -1
                    clause_internal.append(not (sol_list[variable_pos - 1]))

            clause_external.append(clause_internal)
        clause_list_or = [any(clause) for clause in clause_external]  # Doing OR of Variables
        if not satcheck:
            return clause_list_or
        clause_list_and = all(clause_list_or)  # Doing AND of Clauses
        if satcheck:
            return clause_list_and

    def unsat_clauses(self, all_clauses, cnf_formula):
        all_index_unsat_clauses = []
        cnf_formula_unsat = []

        for index, value in enumerate(all_clauses):
            if not value:
                all_index_unsat_clauses.append(index)  # Index of Unsat clauses

        # Now we will find all the clauses which are unsatisfied
        for clause_index in all_index_unsat_clauses:
            cnf_formula_unsat.append(cnf_formula[clause_index])  # List of UNSAT clauses

        return cnf_formula_unsat

    def sat_clauses(self, all_clauses, cnf_formula):
        all_index_sat_clauses = []
        cnf_formula_sat = []

        for index, value in enumerate(all_clauses):
            if value:
                all_index_sat_clauses.append(index)  # Index of sat clauses

        # Now we will find all the clauses which are satisfied
        for clause_index in all_index_sat_clauses:
            cnf_formula_sat.append(cnf_formula[clause_index])  # List of SAT clauses

        return cnf_formula_sat

    def variable_sol_list(self, initial_solution):
        sol_list_init = []
        for index, var in enumerate(initial_solution):
            if not var:
                sol_list_init.append(-1 * (index + 1))
            else:
                sol_list_init.append((index + 1))
        return sol_list_init

    @staticmethod
    def positive_gain(sol_list_init, cnf_formula_unsat):
        positive_gain = []
        for variable in sol_list_init:
            variable_count_unsat = 0

            '''Checking for the unsat clauses which contain the required parameter'''
            for unsat_clause in cnf_formula_unsat:
                if variable in unsat_clause or (-1 * variable) in unsat_clause:
                    variable_count_unsat += 1  # Keeping a count of the clauses

            positive_gain.append(variable_count_unsat)
        return positive_gain

    @staticmethod
    def negative_gain(sol_list_init, cnf_formula_sat, walksat_clause=None):

        negative_gain = []
        temp_sol_list = [False if var < 0 else True for var in sol_list_init]  # Sol list with Boolean values

        if walksat_clause is not None:
            sol_list_init = walksat_clause

        for variable in sol_list_init:
            new_clause_required = []
            variable_list = []

            for sat_clause in cnf_formula_sat:
                if variable in sat_clause or (-1 * variable) in sat_clause:
                    # Creating a temp sat_clause list the sat clauses that contain the required variable
                    temp_sat_clause = sat_clause
                    '''here if the variable is present in the clause, then moving it to the end of the clause 
                    variable list '''
                    if variable in temp_sat_clause:
                        temp_sat_clause.remove(variable)
                        temp_sat_clause.append(variable)
                    else:
                        temp_sat_clause.remove(-1 * variable)
                        temp_sat_clause.append(-1 * variable)

                    # A variable list for all the sat clauses with the required variable pushed to end of list
                    variable_list.append(temp_sat_clause)

            ''' Creating the selected clauses list with boolean values '''
            clause_external_temp = []
            for clause in variable_list:
                clause_internal = []
                for variable_val in clause:
                    if variable_val > 0:  # Checking for the True Values
                        # Checking the truth value at the index in solution file
                        clause_internal.append(temp_sol_list[variable_val - 1])
                    else:  # Checking for the negation values
                        variable_pos = variable_val * -1
                        clause_internal.append(not (temp_sol_list[variable_pos - 1]))

                clause_external_temp.append(clause_internal)  # All clauses for the variable with boolean values

            '''The condition to see if the SAT clause only has the required variable as True'''
            for clause in clause_external_temp:
                if clause[0] is False and clause[1] is False and clause[2] is True:
                    new_clause_required.append(clause)  # Generating the list with only required variable as True

            negative_gain.append(len(new_clause_required))  # generating the negative gain for each variable

        return negative_gain

    @staticmethod
    def final_solution(initial_solution, preprocess, try_sol, flip):
        """ Generating the solution by changing the booleans to actual variable """
        final_sol_list = [i for i in range(1, preprocess.variable_number + 1)]
        for item in range(0, len(initial_solution)):
            if initial_solution[item] is False:
                final_sol_list[item] = final_sol_list[item] * -1
        return final_sol_list


    @staticmethod
    def runtime_plot(runtime, executions, x_label, y_label, plot_title, plot_type='normal'):
        """ To plot the runtime distribution graphs """
        x = runtime     # Values on the x axis
        y = [c / executions for c in range(1, len(runtime) + 1)]    # Values on the y axis

        # Plotting the labels on the graph
        plt.xlabel(x_label)
        plt.ylabel(y_label)

        plt.title(plot_title)    # graph Title
        """Computing the Mean , Median and Standard Deviation"""
        plt.figtext(.8, .8, f'Mean = {round(mean(x),3)}')
        plt.figtext(.8, .7, f'Median = {round(median(x),3)}')
        plt.figtext(.8, .6, f'SD = {round(stdev(x),3)}')

        if plot_type == 'semi_log':
            plt.semilogx(x, y)
        elif plot_type == 'log_log':
            plt.loglog(x, y)
        elif plot_type == 'normal':
            plt.plot(x, y)
        elif plot_type == 'f_rate_log_log':
            y = [1-i for i in y]
            plt.loglog(x, y)

        plt.show()

    @staticmethod
    def input_sanitization(executions, max_tries, max_flips, wp, cutoff_time, cnf_instance, tl=1):

        input_val = [executions, max_tries, max_flips, wp, cutoff_time, tl]

        if not all(isinstance(x, (int, float)) for x in input_val):
            raise TypeError('The input parameters except cnf file name must be a number')

        if not all(i > 0 for i in input_val) :
            raise ValueError('Please enter an input greater than 0')

        if not isinstance(cnf_instance,str):
            raise TypeError('The cnf instance name must be a string value')











