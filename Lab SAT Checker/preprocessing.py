"""
Author: Dheeraj Alimchandani

Date : 13-11-2019

File : preprocessing.py

Usage : Preprocesing the CNF File
"""

# import random
# random.seed(2)


class CnfPreprocess:

    def __init__(self, cnf_instance):

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
