"""
Author: Dheeraj Alimchandani

File : preprocessing.py

Usage : Preprocesing the CNF File
"""


class CnfPreprocess:

    def __init__(self, cnf_instance):
        """
        :param cnf_instance: Contains the cnf instance file
        """

        self.variable_number = 0
        # Opening the cnf instance in read mode
        try:
            with open(cnf_instance, 'r') as sat_file:
                self.variable_number = [clause.strip().split() for clause in sat_file.readlines() if clause.startswith('p')]
                self.variable_number = int(self.variable_number[0][2])  # Extracting the number of variables
                sat_file.seek(0)
                # Taking out the clauses from the cnf file
                self.clause_list = [clause.strip().split() for clause in sat_file.readlines() if
                                    not clause.startswith(('c', 'p', '%', '0'))]
        except FileNotFoundError:
            print('Please enter a valid file name/location')
            exit(0)

    def filter_cnf_instance(self):
        """
        :return: Clause List
        """
        # clause_list contains the clauses
        self.clause_list = list(filter(None, self.clause_list))

        # Converting the clause_list to int
        self.clause_list = [list(map(int, var)) for var in self.clause_list]
        self.clause_list = [var[:-1] for var in self.clause_list]
        return self.clause_list
