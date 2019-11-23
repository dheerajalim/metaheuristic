"""
Author: Dheeraj Alimchandani

Date : 13-11-2019

File : GSAT.py

Usage : GSAT solution
"""

import random


class GSAT:

    @staticmethod
    def positive_gain(sol_list_init, cnf_formula_unsat):
        positive_gain = []
        for variable in sol_list_init:
            variable_count_unsat = 0

            '''Checking fot the unsat clauses which contain the required parameter'''
            for unsat_clause in cnf_formula_unsat:
                if variable in unsat_clause or (-1 * variable) in unsat_clause:
                    variable_count_unsat += 1   # Keeping a count of the clauses

            positive_gain.append(variable_count_unsat)
        return positive_gain

    @staticmethod
    def negative_gain(sol_list_init, cnf_formula_sat):

        negative_gain = []
        temp_sol_list = [False if var < 0 else True for var in sol_list_init]  # Sol list with Boolean values

        for variable in sol_list_init:
            new_clause_required = []
            # print('Variable: ', variable)
            variable_list = []
            # temp_sat_clause = []
            for sat_clause in cnf_formula_sat:
                if variable in sat_clause or (-1 * variable) in sat_clause:
                    # Creating a temp sat_clause list the sat clauses that contain the required variable
                    temp_sat_clause = sat_clause
                    '''here if the variable is present in the clause, then moving it to the end of the clause variable list'''
                    if variable in temp_sat_clause:
                        temp_sat_clause.remove(variable)
                        temp_sat_clause.append(variable)
                    else:
                        temp_sat_clause.remove(-1 * variable)
                        temp_sat_clause.append(-1 * variable)

                    # A variable list for all the sat clauses with the required variable pushed to end of list
                    variable_list.append(temp_sat_clause)
                    # variable_count_sat += 1
            # print('Test', variable_list)

            ''' Creating the selected clauses list with boolean values '''
            clause_external_temp = []
            for clause in variable_list:
                clause_internal = []
                for variable in clause:
                    if variable > 0:  # Checking for the True Values
                        clause_internal.append(
                            temp_sol_list[
                                variable - 1])  # Checking the truth value at the index in solution file
                    else:  # Checking for the negation values
                        variable_pos = variable * -1
                        clause_internal.append(not (temp_sol_list[variable_pos - 1]))

                clause_external_temp.append(clause_internal)  # All clauses for the variable with boolean values
            # print('All clauses :', clause_external_temp)
            # new_clause_required = []
            '''The condition to see if the SAT clause only has the required variable as True'''
            for clause in clause_external_temp:
                if clause[0] is False and clause[1] is False and clause[2] is True:
                    new_clause_required.append(clause)  # Generating the list with only required variable as True

            # print('Required Clause', new_clause_required)
            # print('Required Clause', len(new_clause_required))
            negative_gain.append(len(new_clause_required))  # generating the negative gain for each variable
        # print('Negative Count :', negative_gain)
        return negative_gain

    def gsat_solution(self, cnf_formula, sol_list_init, all_clauses, cnf_formula_unsat):

        # all_index_unsat_clauses = []
        all_index_sat_clauses = []
        # cnf_formula_unsat = []
        cnf_formula_sat = []


        # print(all_clauses)

        # print('Else Loop All Clauses', all_clauses)
        # for index, value in enumerate(all_clauses):
        #     if not value:
        #         all_index_unsat_clauses.append(index)  # Index of Unsat clauses
        #
        # print('Index of UNSAT Clauses : ' , all_index_unsat_clauses)
        #
        # # Now we will find all the clauses which are unsatisfied
        # for clause_index in all_index_unsat_clauses:
        #     cnf_formula_unsat.append(cnf_formula[clause_index])  # List of UNSAT clauses
        # print('UNSAT Clauses: ', cnf_formula_unsat)
        # print('Sol List: ',sol_list_init)

        # now we will calculate the number of clauses in which each variable is present (Positive gain)
        positive_gain = self.positive_gain(sol_list_init, cnf_formula_unsat)
        # print('positive count : ', positive_gain)

        for index, value in enumerate(all_clauses):
            if value:
                all_index_sat_clauses.append(index)  # Index of SAT clauses

        # print('Index of SAT Clauses : ', all_index_sat_clauses)

        for clause_index in all_index_sat_clauses:
            cnf_formula_sat.append(cnf_formula[clause_index])  # List of SAT Clauses
        # print('SAT Clauses: ', cnf_formula_sat)
        # print('Sol List: ',sol_list_init)

        # Now we wil claculate the negative gain
        negative_gain = self.negative_gain(sol_list_init, cnf_formula_sat)

        # Finding the Net Gain value for each variable
        net_gain = [x1 - x2 for (x1, x2) in zip(positive_gain, negative_gain)]
        # print('Net gain: ' , net_gain)

        # getting the maximum netgain
        max_netgain = max(net_gain)
        # print('Maximum value of net gain', max_netgain)

        # Getting the indexes of the maximum net gain value
        max_netgain_list = [i for i, x in enumerate(net_gain) if x == max_netgain]
        # print('Indexes of net gain',max_netgain_list)

        # To choose randomly the maximum net gain variable if more than one max netgain values presetn
        if len(max_netgain_list) > 1:
            net_gain_index = random.choice(max_netgain_list)
            # print('Randomly chosen index of net gain', net_gain_index)
        else:
            net_gain_index = max_netgain_list[0]

        flipped_value_index = net_gain_index
        # print(flipped_value_index)
        # exit()
        return flipped_value_index
