
with open('Lab-data/Lab-data/Inst/uf20-04.cnf', 'r') as sat_file:
    clause_list = [clause.strip().split() for clause in sat_file.readlines() if not clause.startswith(('c','p','%','0'))]

# clause_list contains the clauses
clause_list= list(filter(None,clause_list))


# Converting the clause_list to int
clause_list = [list(map(int, var)) for var in clause_list]
clause_list = [var[:-1] for var in clause_list]


# sol_list contins all the solutions wher -(is False) and +(is True)
with open('Lab-data/Lab-data/sols/1.txt', 'r') as sol_file:
    sol_list = [var.strip().split() for var in sol_file.readlines() if not var.startswith(('c'))]

'''Filtering the sol list as per the requirement'''
for variables in sol_list:
    variables.remove('v')
sol_list = sol_list[:-1]
sol_list = [int(var) for sub_var in sol_list for var in sub_var]

'''Filtering Ends '''

'''Converting the sol_list to truth values'''
sol_list = [False if var < 0 else True for var in sol_list]

clause_list_clauses = list(clause_list)

clause_external = []
for clause in clause_list:
    clause_internal = []
    for variable in clause:
        if variable > 0:
            clause_internal.append(sol_list[variable-1])
        else:
            variable_pos = variable*-1
            clause_internal.append(not(sol_list[variable_pos-1]))

    clause_external.append(clause_internal)


clause_list_or = [any(clause) for clause in clause_external]

clause_list_and = all(clause_list_or)


# unsat_clauses = [clause_list_or.index(unsat_clause) for unsat_clause in clause_list_or if unsat_clause is False]
unsat_clauses = [index for index, unsat_clause in enumerate(clause_list_or) if unsat_clause is False]
if clause_list_and:
    print('The provided solution in valid')
else:
    print('The provided solution is invalid')
    print('The Unsatisfied clauses are :')
    print('Clauses: ', unsat_clauses)

    for index in unsat_clauses:
        print(clause_list_clauses[index])



