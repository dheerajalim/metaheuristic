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

    def gsat_solution(self, cnf_formula, max_tries, max_flips):
        for try_sol in range(0, max_tries):

            a = self.generate_solution()  # Here we will generate the random solution in the form of Booleans
            print('Initial Solution :', a)


            initial_flipped = 0
            for flip in range(0, max_flips):

                if self.clause_satisfation(a, satcheck = True):      # Here we will be returned with the and of all clauses
                    ''' Generating the solution by changing the booleans to actual variable '''
                    final_sol_list = [i for i in range(1, self.variable_number + 1)]
                    for item in range(0, len(a)):
                        if a[item] is False:
                            final_sol_list[item] = final_sol_list[item] * -1
                    self.sat_variables = final_sol_list
                    return f'Solution is {final_sol_list} generated in {try_sol} tries'

                else:
                    all_index_unsat_clauses = []
                    all_index_sat_clauses = []
                    cnf_formula_unsat = []
                    cnf_formula_sat = []
                    positive_gain = []
                    negative_gain = []
                    sol_list_init = []
                    for index, var in enumerate(a):
                        if not var:
                            sol_list_init.append(-1 * (index + 1))
                        else:
                            sol_list_init.append((index + 1))

                    all_clauses = self.clause_satisfation(a, satcheck=False)

                    print('Else Loop All Clauses', all_clauses)
                    for index,value in enumerate(all_clauses):
                        if not value:
                            all_index_unsat_clauses.append(index)

                    print('Index of UNSAT Clauses : ' , all_index_unsat_clauses)
                    # Now we will find all the clauses which are unsatisfied
                    for clause_index in all_index_unsat_clauses:
                        cnf_formula_unsat.append(cnf_formula[clause_index])
                    print('UNSAT Clauses: ', cnf_formula_unsat)
                    print('Sol List: ',sol_list_init)

                    # now we will calculate the number of clauses in which each variable is present (Positive gain)
                    for variable in sol_list_init:
                        variable_count_unsat = 0

                        for unsat_clause in cnf_formula_unsat:
                            if variable in unsat_clause or (-1*variable) in unsat_clause:
                                variable_count_unsat += 1

                        positive_gain.append(variable_count_unsat)

                    print('positive count : ', positive_gain)


                    # now flip the entire sol list
                    for index,value in enumerate(all_clauses):
                        if value:
                            all_index_sat_clauses.append(index)

                    print('Index of SAT Clauses : ', all_index_sat_clauses)
                    for clause_index in all_index_sat_clauses:
                        cnf_formula_sat.append(cnf_formula[clause_index])
                    print('SAT Clauses: ', cnf_formula_sat)
                    print('Sol List: ',sol_list_init)
                    temp_sol_list = [False if var < 0 else True for var in sol_list_init]

                    #
                    for variable in sol_list_init:
                        new_clause_required = []
                        print('Variable: ', variable)
                        variable_count_sat = 0
                        # variable = 3
                        variable_count_sat = 0
                        variable_list = []
                        # temp_sat_clause = []
                        for sat_clause in cnf_formula_sat:
                            if variable in sat_clause or (-1*variable) in sat_clause:
                                temp_sat_clause = sat_clause
                                if variable in temp_sat_clause:
                                    temp_sat_clause.remove(variable)
                                    temp_sat_clause.append(variable)
                                else:
                                    temp_sat_clause.remove(-1*variable)
                                    temp_sat_clause.append(-1*variable)

                                # variable_list.append(sat_clause)
                                variable_list.append(temp_sat_clause)
                                # variable_count_sat += 1
                        print('Test', variable_list)

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

                            clause_external_temp.append(clause_internal)
                        print('All clauses :', clause_external_temp)
                        # new_clause_required = []
                        for clause in clause_external_temp:
                            if clause[0] is False and clause[1] is False and clause[2] is True:
                                new_clause_required.append(clause)

                        print('Required Clause', new_clause_required)
                        print('Required Clause', len(new_clause_required))
                        negative_gain.append(len(new_clause_required))
                    print('Negative Count :', negative_gain)
                    # exit()
                    # negative_gain.append(variable_count_sat)
                    # print('after flipping to last : ' , variable_list)
                    # print('Negative count: ', negative_gain)
                    # # temp_sol_list = [False if var < 0 else True for var in sol_list_init]
                    # print('Temp sol:', temp_sol_list)

                    # clause_external_temp = []
                    # for clause in variable_list:
                    #     clause_internal = []
                    #     for variable in clause:
                    #         if variable > 0:  # Checking for the True Values
                    #             clause_internal.append(
                    #                 temp_sol_list[variable - 1])  # Checking the truth value at the index in solution file
                    #         else:  # Checking for the negation values
                    #             variable_pos = variable * -1
                    #             clause_internal.append(not (temp_sol_list[variable_pos - 1]))
                    #
                    #     clause_external_temp.append(clause_internal)
                    # print('All clauses :', clause_external_temp)

                    # new_clause_required = []
                    # for clause in clause_external_temp:
                    #     if clause[0] is False and clause[1] is False and clause[2] is True:
                    #         new_clause_required.append(clause)
                    #
                    # print('Required Clause', new_clause_required)
                    # exit()
                    # sol_list_init = [sol*-1 for sol in sol_list_init]
                    # print('Flipped sol list: ', sol_list_init)
                    # for variable in sol_list_init:
                    #     variable_count_unsat = 0
                    #     for unsat_clause in cnf_formula_unsat:
                    #         if variable in unsat_clause:
                    #             variable_count_unsat += 1
                    #
                    #     negative_gain.append(variable_count_unsat)
                    # print('negative count : ', negative_gain)
                    net_gain = [x1 - x2 for (x1, x2) in zip(positive_gain, negative_gain)]
                    print('Net gain: ' , net_gain)

                    max_netgain = max(net_gain)
                    print('Maximum occurance of net gain', max_netgain)

                    max_netgain_list = [i for i, x in enumerate(net_gain) if x == max_netgain]
                    print('Indexes of net gain',max_netgain_list)

                    net_gain_index = random.choice(max_netgain_list)
                    print('Randomly chosen index of net gain', net_gain_index)

                    flipped_value = net_gain_index
                    a[flipped_value] = not (a[flipped_value])
                    print('Flipped solution', a)

                    # exit()
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
    max_tries = 10
    max_flips = 1000
    cnf_instance = 'Lab-data/Lab-data/Inst/uf20-06.cnf'
    gsat_algo = GsatAlgo(cnf_instance)
    cnf_formula = gsat_algo.filter_cnf_instance()
    # print(cnf_formula)  # Contains the cleaned list of cnf formulas
    result = gsat_algo.gsat_solution(cnf_formula, max_tries, max_flips)
    print(result)
    gsat_algo.solution_txt()
