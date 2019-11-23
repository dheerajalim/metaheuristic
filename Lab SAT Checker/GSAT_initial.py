import random


global sol_list_orig

random.seed(2)
with open('Lab-data/Lab-data/Inst/uf20-06.cnf', 'r') as sat_file:
    variable_number = [clause.strip().split() for clause in sat_file.readlines() if  clause.startswith('p')]
    variable_number = int(variable_number[0][2])
    sat_file.seek(0)
    clause_list = [clause.strip().split() for clause in sat_file.readlines() if
                   not clause.startswith(('c', 'p', '%', '0'))]


# clause_list contains the clauses
clause_list= list(filter(None,clause_list))

# Converting the clause_list to int
clause_list = [list(map(int, var)) for var in clause_list]
clause_list = [var[:-1] for var in clause_list]

# print(clause_list)
# print(variable_number)
clause_list_clauses = list(clause_list)

# sol_list = [i for i in range(1,variable_number+1)]
# # print(sol_list)
#
# for solution in range(0,len(sol_list)):
#     if random.random() < 0.5:
#         sol_list[solution] = -1*sol_list[solution]
#
# # print(sol_list)
# '''Converting the sol_list to truth values'''
# sol_list_orig = sol_list
# sol_list = [False if var < 0 else True for var in sol_list]
# # print(sol_list)

def random_sol():
    sol_list = [i for i in range(1, variable_number + 1)]
    # print(sol_list)

    for solution in range(0, len(sol_list)):
        if random.random() < 0.5:
            sol_list[solution] = -1 * sol_list[solution]

    # print(sol_list)
    '''Converting the sol_list to truth values'''
    sol_list = [False if var < 0 else True for var in sol_list]
    # print(sol_list)

    return sol_list

def clause_satisfation(sol_list):
    global clause_list_or
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

    # print(clause_list_or)

    return clause_list_and

max_tries = 100
max_flips = 10

# clause_satisfation(sol_list)


def gsat_solution(max_tries, max_flips):

    for try_sol in range(0,max_tries):
        a = random_sol()
        print('New Loop Sol', a)
        initial_flipped = 0
        for flip in range(0,max_flips):
            print('Initial Solution ', a)
            if clause_satisfation(a):
                print(f'The satisfied sol came in {try_sol} steps')
                final_sol_list = [i for i in range(1, variable_number + 1)]

                for item in range(0,len(a)):
                    if a[item] is False:
                        final_sol_list[item] = final_sol_list[item]*-1

                print(final_sol_list)
                return a
            else:

                unsatisified_clauses = []
                unsat_clauses = [index for index, unsat_clause in enumerate(clause_list_or) if unsat_clause is False]
                print('Unsat Clauses Index', unsat_clauses)
                for index in unsat_clauses:
                    unsatisified_clauses.append(clause_list_clauses[index])
                print('Unsatisfied clauses', unsatisified_clauses)
                flat_unsatisified_clauses = [item for sublist in unsatisified_clauses for item in sublist]
                print('Flat Unsatisfied List',sorted(flat_unsatisified_clauses))
                fliped_value = max(set(flat_unsatisified_clauses), key=flat_unsatisified_clauses.count)
                print('Maximum Occurance of: ',fliped_value)
                print('Initial Flipped', initial_flipped)
                if initial_flipped == abs(fliped_value):
                    # fliped_value = flat_unsatisified_clauses[0]
                    fliped_value = random.choice(flat_unsatisified_clauses)
                    initial_flipped = abs(fliped_value)
                else:
                    initial_flipped = abs(fliped_value)
                print('Final Flipped Value', fliped_value)
                print('Original Sol', a)
                if fliped_value < 0:
                    fliped_value = fliped_value * -1
                a[fliped_value-1] = not(a[fliped_value-1])
                print('Flipped Sol', a)
    return ('No solution')


print(gsat_solution(max_tries,max_flips))