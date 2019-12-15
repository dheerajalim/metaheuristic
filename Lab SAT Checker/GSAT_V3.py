"""
Author: Dheeraj Alimchandani

Date : 13-11-2019

"""
import random

random.seed(2)


class GsatAlgo:

    def __init__(self, cnf_instance):
        self.clause_external = []
        self.clause_list_or = []
        self.clause_list_and = []
        self.sat_variables = []
        self.variable_number = 0
        # self.sol_list_init = []

        with open(cnf_instance, 'r') as sat_file:
            self.variable_number = [clause.strip().split() for clause in sat_file.readlines() if clause.startswith('p')]
            self.variable_number = int(self.variable_number[0][2])
            sat_file.seek(0)
            self.clause_list = [clause.strip().split() for clause in sat_file.readlines() if
                                not clause.startswith(('c', 'p', '%', '0'))]

    def filter_cnf_instance(self):
        # clause_list contains the clauses
        self.clause_list = list(filter(None, self.clause_list))

        # Converting the clause_list to int
        self.clause_list = [list(map(int, var)) for var in self.clause_list]
        self.clause_list = [var[:-1] for var in self.clause_list]
        return self.clause_list

    def generate_solution(self):
        self.sol_list_init = []
        sol_list = [i for i in range(1, self.variable_number + 1)]
        for solution in range(0, len(sol_list)):
            if random.random() < 0.5:
                sol_list[solution] = -1 * sol_list[solution]
        self.sol_list_init = sol_list # Creating a copy of generated sol list before changing it to boolean
        '''Converting the sol_list to truth values'''
        sol_list = [False if var < 0 else True for var in sol_list]
        return sol_list

    def clause_satisfation(self, sol_list, satcheck):
        """
        The function is responsible to generate the truth values in the clause list based on the solution list
        """
        self.clause_external = []
        for clause in self.clause_list:
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

    def solution(self, cnf_formula, initial_flipped):
        unsatisified_clauses = []
        unsat_clauses = [index for index, unsat_clause in enumerate(self.clause_list_or) if unsat_clause is False]

        for index in unsat_clauses:
            unsatisified_clauses.append(cnf_formula[index])

        flat_unsatisified_clauses = [item for sublist in unsatisified_clauses for item in sublist]
        fliped_value = max(set(flat_unsatisified_clauses), key=flat_unsatisified_clauses.count)
        if initial_flipped == abs(fliped_value):
            fliped_value = random.choice(flat_unsatisified_clauses)
            initial_flipped = abs(fliped_value)
        else:
            initial_flipped = abs(fliped_value)
        if fliped_value < 0:
            fliped_value = fliped_value * -1

        return fliped_value, initial_flipped

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
    def negative_gain(sol_list_init,cnf_formula_sat):

        negative_gain = []
        temp_sol_list = [False if var < 0 else True for var in sol_list_init] # Sol list with Boolean values

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
            negative_gain.append(len(new_clause_required))      # generating the negative gain for each variable
        # print('Negative Count :', negative_gain)
        return negative_gain


    def gsat_solution(self, cnf_formula, max_tries, max_flips):
        for try_sol in range(0, max_tries):

            a = self.generate_solution()  # Here we will generate the random solution in the form of Booleans
            # print('Initial Solution :', a)

            for flip in range(0, max_flips):

                if self.clause_satisfation(a, satcheck = True):      # Here we will be returned with the and of all clauses
                    ''' Generating the solution by changing the booleans to actual variable '''
                    final_sol_list = [i for i in range(1, self.variable_number + 1)]
                    for item in range(0, len(a)):
                        if a[item] is False:
                            final_sol_list[item] = final_sol_list[item] * -1
                    self.sat_variables = final_sol_list
                    return f'Solution is {final_sol_list} generated in {try_sol+1} tries and {max_flips+1} flips'

                else:
                    all_index_unsat_clauses = []
                    all_index_sat_clauses = []
                    cnf_formula_unsat = []
                    cnf_formula_sat = []
                    sol_list_init = []

                    # Generating the variable solution list from the boolean list
                    for index, var in enumerate(a):
                        if not var:
                            sol_list_init.append(-1 * (index + 1))
                        else:
                            sol_list_init.append((index + 1))
                    # print(sol_list_init)
                    # print(a)

                    # List of all the clauses after performing OR operation on each
                    all_clauses = self.clause_satisfation(a, satcheck=False)
                    # print(all_clauses)

                    # print('Else Loop All Clauses', all_clauses)
                    for index,value in enumerate(all_clauses):
                        if not value:
                            all_index_unsat_clauses.append(index)       # Index of Unsat clauses

                    # print('Index of UNSAT Clauses : ' , all_index_unsat_clauses)

                    # Now we will find all the clauses which are unsatisfied
                    for clause_index in all_index_unsat_clauses:
                        cnf_formula_unsat.append(cnf_formula[clause_index])  # List of UNSAT clauses
                    # print('UNSAT Clauses: ', cnf_formula_unsat)
                    # print('Sol List: ',sol_list_init)

                    # now we will calculate the number of clauses in which each variable is present (Positive gain)
                    positive_gain = self.positive_gain(sol_list_init,cnf_formula_unsat)
                    # print('positive count : ', positive_gain)

                    for index,value in enumerate(all_clauses):
                        if value:
                            all_index_sat_clauses.append(index) # Index of SAT clauses

                    # print('Index of SAT Clauses : ', all_index_sat_clauses)

                    for clause_index in all_index_sat_clauses:
                        cnf_formula_sat.append(cnf_formula[clause_index]) # List of SAT Clauses
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

                    flipped_value = net_gain_index
                    a[flipped_value] = not (a[flipped_value])   # Fliiping the variable in the solution list
                    # print('Flipped solution', a)


                    # fliped_value, initial_flipped = self.solution(cnf_formula, initial_flipped)
                    # a[fliped_value - 1] = not (a[fliped_value - 1])

        return 'No Solution'

    def solution_txt(self):
        with open('sol.txt', 'w') as sat_sol:
            sat_sol.write('c Solution generated using GSAT \n')
            sat_sol.write('v')
            for variables in self.sat_variables:
                if variables % 11 == 0:
                    sat_sol.write('\n')
                    sat_sol.write('v')
                sat_sol.write(f' {str(variables)} ')


if __name__ == '__main__':
    max_tries = 100
    max_flips = 7
    cnf_instance = 'Lab-data/Lab-data/Inst/uf20-06.cnf'
    gsat_algo = GsatAlgo(cnf_instance)
    cnf_formula = gsat_algo.filter_cnf_instance()
    # print(cnf_formula)  # Contains the cleaned list of cnf formulas
    result = gsat_algo.gsat_solution(cnf_formula, max_tries, max_flips)
    print(result)
    gsat_algo.solution_txt()
