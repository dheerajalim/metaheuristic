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
        sol_list = [i for i in range(1, self.variable_number + 1)]
        for solution in range(0, len(sol_list)):
            if random.random() < 0.5:
                sol_list[solution] = -1 * sol_list[solution]
        '''Converting the sol_list to truth values'''
        sol_list = [False if var < 0 else True for var in sol_list]
        return sol_list

    def clause_satisfation(self, sol_list):
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
        self.clause_list_or = [any(clause) for clause in self.clause_external]  # Doing OR of Variables
        self.clause_list_and = all(self.clause_list_or)  # Doing AND of Clauses
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
            a = self.generate_solution()

            initial_flipped = 0
            for flip in range(0, max_flips):

                if self.clause_satisfation(a):
                    final_sol_list = [i for i in range(1, self.variable_number + 1)]
                    for item in range(0, len(a)):
                        if a[item] is False:
                            final_sol_list[item] = final_sol_list[item] * -1
                    self.sat_variables = final_sol_list
                    return f'Solution is {final_sol_list} generated in {try_sol} tries'

                else:
                    fliped_value, initial_flipped = self.solution(cnf_formula, initial_flipped)
                    a[fliped_value - 1] = not (a[fliped_value - 1])

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
    max_flips = 10
    cnf_instance = 'Lab-data/Lab-data/Inst/uf20-06.cnf'
    gsat_algo = GsatAlgo(cnf_instance)
    cnf_formula = gsat_algo.filter_cnf_instance()
    result = gsat_algo.gsat_solution(cnf_formula, max_tries, max_flips)
    print(result)
    gsat_algo.solution_txt()
