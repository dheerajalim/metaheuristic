"""
Author: Dheeraj Alimchandani

Date : 12-11-2019

"""
class SatChecker:

    def __init__(self, cnf_instance, solution_file):
        self.clause_external = []
        self.clause_list_or = []
        self.clause_list_and = []
        self.clause_list_clauses = []

        with open(cnf_instance, 'r') as sat_file:
            self.clause_list = [clause.strip().split() for clause in sat_file.readlines() if
                                not clause.startswith(('c', 'p', '%', '0'))]

        # sol_list contains all the solutions where -(is False) and +(is True)
        with open(solution_file, 'r') as sol_file:
            self.sol_list = [var.strip().split() for var in sol_file.readlines() if not var.startswith('c')]

        self.filter_cnf_instance()
        self.filter_solution_file()
        self.cnf_truth_values()

    def filter_cnf_instance(self):
        # clause_list contains the clauses
        self.clause_list = list(filter(None, self.clause_list))

        # Converting the clause_list to int
        self.clause_list = [list(map(int, var)) for var in self.clause_list]
        self.clause_list = [var[:-1] for var in self.clause_list]

    def filter_solution_file(self):
        for variables in self.sol_list:
            variables.remove('v')
        self.sol_list = self.sol_list[:-1]
        self.sol_list = [int(var) for sub_var in self.sol_list for var in sub_var]

        '''Converting the sol_list to truth values'''
        self.sol_list = [False if var < 0 else True for var in self.sol_list]

    def cnf_truth_values(self):
        """
        The function is responsible to generate the truth values in the clause list based on the solution list
        """
        self.clause_list_clauses = list(self.clause_list)
        for clause in self.clause_list:
            clause_internal = []
            for variable in clause:
                if variable > 0:    # Checking for the True Values
                    clause_internal.append(self.sol_list[variable - 1]) # Checking the truth value at the index in solution file
                else:               # Checking for the negation values
                    variable_pos = variable * -1
                    clause_internal.append(not (self.sol_list[variable_pos - 1]))

            self.clause_external.append(clause_internal)

    def solution(self):
        self.clause_list_or = [any(clause) for clause in self.clause_external]  # Doing OR of Variables
        self.clause_list_and = all(self.clause_list_or) # Doing AND of Clauses
        unsat_clauses = [index for index, unsat_clause in enumerate(self.clause_list_or) if unsat_clause is False]
        if self.clause_list_and:
            print('The provided solution in valid')
        else:
            print('The provided solution is invalid')
            print('The Unsatisfied clauses are :')
            print('Clauses: ', unsat_clauses)

            for index in unsat_clauses:
                print(self.clause_list_clauses[index])


if __name__ == '__main__':
    cnf_instance = 'Lab-data/Lab-data/Inst/uf20-04.cnf'
    solution_file = 'Lab-data/Lab-data/sols/2.txt'
    sat_checker = SatChecker(cnf_instance,solution_file)
    sat_checker.solution()