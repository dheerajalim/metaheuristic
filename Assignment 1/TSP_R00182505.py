"""
Author: Dheeraj Alimchandani
file: TSP_R00182505
"""

import random
from Individual import *
import sys
import time
import itertools

myStudentNum = 'R00182505'
random.seed(myStudentNum)

class BasicTSP:
    def __init__(self, _fName, _popSize, _mutationRate, _maxIterations,
                 _initialSolution, _selection, _crossoverType, _mutationType):
        """
        Parameters and general variables
        """
        self.population     = []
        self.matingPool     = []
        self.matingPool_sus = {}
        self.best           = None
        self.popSize        = _popSize
        self.genSize        = None
        self.mutationRate   = _mutationRate
        self.maxIterations  = _maxIterations
        self.iteration      = 0
        self.fName          = _fName
        self.data           = {}

        """
        Parameters for running Genetic Algorithm with different combination
        """
        self.initialSolution = _initialSolution
        self.selection = _selection
        self.crossoverType = _crossoverType
        self.mutationType = _mutationType

        self.readInstance()
        self.initPopulation()

    def readInstance(self):
        """
        Reading an instance from fName
        """
        file = open(self.fName, 'r')
        self.genSize = int(file.readline())
        self.data = {}
        for line in file:
            (id, x, y) = line.split()
            self.data[int(id)] = (int(x), int(y))
        file.close()

    def initPopulation(self):
        """
        Creating random/heuristic individuals in the population
        self.initialSolution == 0 implies the initial population is generated using Random selection Approach
        self.initialSolution == 1 implies the initial population is generated using Heuristic Approach
        """

        for i in range(0, self.popSize):
            individual = Individual(self.genSize, self.data, self.initialSolution)
            individual.computeFitness()
            self.population.append(individual)

        self.best = self.population[0].copy()
        for ind_i in self.population:
            if self.best.getFitness() > ind_i.getFitness():
                self.best = ind_i.copy()
        print ("Best initial sol: ",self.best.getFitness())

        # Writing the details into a file.
        file.write(f'Best initial sol: {self.best.getFitness()}')
        file.write('\n')

    def updateBest(self, candidate):
        """
        Updates the best candidate's fitness in self.best
        :param candidate: Object of Individual Class
        :return: None
        """
        if self.best == None or candidate.getFitness() < self.best.getFitness():
            self.best = candidate.copy()
            # print ("iteration: ",self.iteration, "best: ",self.best.getFitness(), "path: ", self.best.genes)
            print ("iteration: ",self.iteration, "best: ",self.best.getFitness())

            file.write(f'iteration: {self.iteration} best: {self.best.getFitness()}')
            file.write('\n')
        # else:
        #     print('current fitness = ', candidate.getFitness())
        #     print('best solution yet = ',self.best.getFitness())

    def randomSelection(self):
        """
        Random (uniform) selection of two individuals
        """
        indA = self.matingPool[ random.randint(0, self.popSize-1) ]
        indB = self.matingPool[ random.randint(0, self.popSize-1) ]
        return [indA, indB]

    def stochasticUniversalSampling(self):
        """
        Implementation of Stochastic Universal Sampling
        :return: Two selected parents from the mating pool generated using selection probability
        """

        N_parent = 2                    # Need to select two Parents
        distance_pointers = 1/N_parent
        indA_pointer = random.uniform(0,distance_pointers) # Selection of random starting pointer
        indB_pointer = indA_pointer + distance_pointers    # Selection of 2nd pointer

        # print(self.matingPool_sus)
        # print(indA_pointer)
        # print(indB_pointer)
        # print(self.ind_selection_range)

        parent_test = True
        for pointer in self.ind_selection_range:
            if parent_test:
                if indA_pointer < pointer:

                    parent_a = self.population[self.ind_selection_range.index(pointer)]
                    parent_test = False

            if indB_pointer < pointer:
                parent_b = self.population[self.ind_selection_range.index(pointer)]
                break

        # parent_test = True
        # for ind,pointer in self.matingPool_sus.items():
        #     if parent_test:
        #         if indA_pointer < pointer:
        #             parent_a = ind
        #             parent_test = False
        #             continue
        #     if indB_pointer < pointer:
        #         parent_b = ind
        #         break

        return [parent_a, parent_b]

    def uniformCrossover(self, indA, indB):

        """
        :param indA: Parent A
        :param indB:  Parent B
        :return: Returns 2 offsprings after perfroming uniform Crossover on the Parent A and B
        """

        pos_list = []  # Creating a list to contain the randomly selected locations that will not change.

        pos_nochange = random.randint(0,self.genSize)
        for num in range(0, pos_nochange):
            pos_list.append(random.randint(0, self.genSize  - 1))   # Selecting pos_nochange random locations

        # Initializing the offspring list with -1 in order to fill the changeable genes
        offspring_A = list(itertools.repeat(-1, self.genSize))
        offspring_B = list(itertools.repeat(-1, self.genSize))

        # Updating the offsprings with the genes that are non changeable
        for x in pos_list:
            offspring_A[x] = indA.genes[x]
            offspring_B[x] = indB.genes[x]

        # Updating the offsprings with the genes from alternative parent that are not already present in the offspring
        for item in indB.genes:
            if item not in offspring_A:
                offspring_A[offspring_A.index(-1)] = item

        for item in indA.genes:
            if item not in offspring_B:
                offspring_B[offspring_B.index(-1)] = item

        '''To handle the list of child. Converting it to object of type Individual'''
        child_a = indA.copy()
        child_b = indB.copy()
        for i in range(0, self.genSize):
            child_a.genes[i] = offspring_A[i]
            child_b.genes[i] = offspring_B[i]
        return child_a, child_b

    def pmxCrossover(self, indA, indB):
        """
        :param indA: Parent A
        :param indB: Parent B
        :return: Returns 2 offsprings after performing PMX Crossover on the Parent A and B
        """
        # Taking the random indexes to select genes that will reverse in the offspring
        indexB = random.randint(0, self.genSize - 1)
        indexA = random.randint(0, indexB)

        # Creating a mapping space for the reversed genes:
        map_indA = {}
        map_indB = {}

        # Creating the copy of original Parent
        indA_orig = indA.copy()
        indB_orig = indB.copy()

        # The below is used to create the Mapping for the genes which were swapped in offsprings
        for x in range(indexA, indexB + 1):
            tmp = indA.genes[x]
            indA.genes[x] = indB.genes[x]
            indB.genes[x] = tmp
            map_indA[indA.genes[x]] = indB.genes[x]

        for key, value in map_indA.items():
            map_indB[value] = key

        # Replacing the genes with more than one occurrence to -1
        for i in range(0, self.genSize):
            if indexA <= i <= indexB:
                continue
            else:
                if indA.genes.count(indA.genes[i]) > 1:
                    indA.genes[i] = -1
                if indB.genes.count(indB.genes[i]) > 1:
                    indB.genes[i] = -1

        """
        pmx_mapper function to handle the mapping cycle
        """
        self.pmx_mapper(indA_orig, indA, 'A',map_indA, map_indB)
        self.pmx_mapper(indB_orig, indB, 'B', map_indA, map_indB)

        return indA, indB

    def pmx_mapper(self,ind_orig, ind, parent, map_indA, map_indB):
        """
        :param ind_orig: Original Parent
        :param ind: Modified Parent
        :param parent: Parent Type A or B
        :param map_indA: Mapping for Parent A
        :param map_indB: Mapping for Paren B
        :return: Updated individual after the mapping cycle procedure
        """

        for x in range(0, self.genSize):
            mapping_loop = True
            if ind.genes[x] == -1:
                if parent == 'A':
                    mapper = map_indA[ind_orig.genes[x]]
                elif parent == 'B':
                    mapper = map_indB[ind_orig.genes[x]]
                while mapping_loop:                     # Searches for the appropriate cycle to be used
                    if mapper in ind.genes:
                        if parent == 'A':
                            mapper = map_indA[mapper]
                        elif parent == 'B':
                            mapper = map_indB[mapper]
                    else:
                        mapping_loop = False

                ind.genes[x] = mapper

    def reciprocalExchangeMutation(self, indA, indB):
        """
         Mutate an individual by swaping two cities with certain probability (i.e., mutation rate)
        :param indA: Parent A
        :param indB: Parent B
        :return: Offspring with mutation performed on it
        """
        # self.mutation(indA, indB)

        # Checks if the mutation rate is acheived
        if random.random() > self.mutationRate:
            indA.computeFitness()
            self.updateBest(indA)
            indB.computeFitness()
            self.updateBest(indB)
            return

        indexA = random.randint(0, self.genSize - 1)
        indexB = random.randint(0, self.genSize - 1)

        # This method is used to swap the values in the Reciprocal Mutation process for the Child
        self.reciprocal_mutation_flip(indA, indexA, indexB)
        self.reciprocal_mutation_flip(indB, indexA, indexB)

    def reciprocal_mutation_flip(self, ind, indexA, indexB):
        """
        This method is used to swap the values in the Reciprocal Mutation process for the Child
        :param ind: Parent
        :param indexA: Index location 1
        :param indexB: Index location 2
        :return: offspring with cities swapped
        """
        tmp = ind.genes[indexA]
        ind.genes[indexA] = ind.genes[indexB]
        ind.genes[indexB] = tmp
        ind.computeFitness()
        self.updateBest(ind)

    def inversionMutation(self, indA, indB):
        """
        Mutate the individual by inversing the order of cities between two points
        :param indA: Parent A
        :param indB: Parent B
        :return: 2 Offspring after mutation
        """

        if random.random() > self.mutationRate:
            indA.computeFitness()
            self.updateBest(indA)
            indB.computeFitness()
            self.updateBest(indB)
            return

        indexA = random.randint(0, self.genSize-1)
        indexB = random.randint(0, self.genSize-1)

        # Reversing the order of the cities between indexA and indexB
        if indexA > indexB:

            indA.genes[indexB:indexA+1] = indA.genes[indexB:indexA+1][::-1]
            indB.genes[indexB:indexA+1] = indB.genes[indexB:indexA+1][::-1]

        elif indexA < indexB:

            indA.genes[indexA:indexB + 1] = indA.genes[indexA:indexB + 1][::-1]
            indB.genes[indexA:indexB + 1] = indB.genes[indexA:indexB + 1][::-1]

        # In case indexA = indexB , no impact on the individual.

        indA.computeFitness()
        self.updateBest(indA)
        indB.computeFitness()
        self.updateBest(indB)

    def crossover(self, indA, indB):
        # NOT USED
        """
        Executes a 1 order crossover and returns a new individual
        """
        child = []
        tmp = {}

        indexA = random.randint(0, self.genSize-1)
        indexB = random.randint(0, self.genSize-1)

        for i in range(0, self.genSize):
            if i >= min(indexA, indexB) and i <= max(indexA, indexB):
                tmp[indA.genes[i]] = False
            else:
                tmp[indA.genes[i]] = True
        aux = []
        for i in range(0, self.genSize):
            if not tmp[indB.genes[i]]:
                child.append(indB.genes[i])
            else:
                aux.append(indB.genes[i])
        child += aux

        '''To handle the list of child. Converting it to object of type Individual'''
        child_obj = indA.copy()
        for i in range(0,self.genSize):
            child_obj.genes[i] = child[i]

        return child_obj

    def mutation(self, indA, indB):
        # NOT USED
        # This works as per the reciprocal Exchange
        """
        Mutate an individual by swaping two cities with certain probability (i.e., mutation rate)
        """

        if random.random() > self.mutationRate:
            indA.computeFitness()
            self.updateBest(indA)
            indB.computeFitness()
            self.updateBest(indB)
            return

        indexA = random.randint(0, self.genSize-1)
        indexB = random.randint(0, self.genSize-1)

        self.reciprocal_mutation_flip(indA, indexA, indexB)
        self.reciprocal_mutation_flip(indB, indexA, indexB)

    def updateMatingPool(self):
        """
        Updating the mating pool before creating a new generation

        if self.selection == 0 : Mating pool generated using Random Selection
        if self.selection == 1: Mating pool generated using Stochastic Universal Sampling
        """
        if self.selection == 0 :
            self.matingPool = []
            for ind_i in self.population:
                self.matingPool.append(ind_i.copy())

        elif self.selection == 1:
            # self.matingPool_sus = {}
            fitness_list = []
            minimize_fitness_list = []
            selection_probability_fitness_list = []

            # Creating a list to hold the fitness of each ind in population
            for ind_i in self.population:
                fitness_list.append(ind_i.getFitness())

            # Getting the max fitness from the list of ind fitness
            max_fitness = max(fitness_list) + 1 # Adding 1 to avoid value to turn 0 on subtraction

            # Minimizing the fitness of ind
            for fitness in fitness_list:
                minimize_fitness_list.append(max_fitness - fitness)

            fitness_sum = sum(minimize_fitness_list)

            # Generating the Selection probability for the individual
            for fitness in minimize_fitness_list:
                selection_probability_fitness_list.append(fitness/fitness_sum)

            # Generating the selection range of the ind
            self.ind_selection_range = [selection_probability_fitness_list[0]]

            for fitness in range(1,len(selection_probability_fitness_list)):
                self.ind_selection_range.append(self.ind_selection_range[fitness-1] + selection_probability_fitness_list[fitness])

            # print('initial_mating = ', self.matingPool_sus)
            # Now we need to create a dictionary of mating pool with each individual and its selection probability
            # print('population = ', self.population)
            # for i in range(0,len(self.population)):
            #     self.matingPool_sus[self.population[i]] = ind_selection_range[i]
            # print('Mating Pool = ',len(self.matingPool_sus))


    def newGeneration(self):
        """
        Creating a new generation
        1. Selection
            a. randomSelection
            b. stochasticUniversalSampling
        2. Crossover
            a. uniformCrossover
            b. pmxCrossover
        3. Mutation
            a. inversionMutation
            b. reciprocalExchangeMutation
        """
        offspring_population = []
        # for i in range(0, len(self.population), 2):
        for i in range(0, len(self.population)):
            """
            Random Selection or SUS selection
            """
            if self.selection == 0:
                partnerA, partnerB = self.randomSelection()

            elif self.selection == 1:
                partnerA, partnerB = self.stochasticUniversalSampling()

            """
            Uniform Crossover or PMX crossover
            """
            if self.crossoverType == 0:
                child_a, child_b = self.uniformCrossover(partnerA, partnerB)

            elif self.crossoverType == 1:
                child_a, child_b = self.pmxCrossover(partnerA, partnerB)

            """
            Inversion or Reciprocal Exchange Mutation
            """
            if self.mutationType == 0:
                self.inversionMutation(child_a, child_b)

            elif self.mutationType == 1:
                self.reciprocalExchangeMutation(child_a, child_b)

            """
            Generation of new population by adding the two children
            """

            # self.population[i] = child_a
            # self.population[i+1] = child_b

            offspring_population.append(child_a)
            offspring_population.append(child_b)

        for i in range(0, len(self.population)):
            self.population[i] = random.choice(offspring_population)


    def GAStep(self):
        """
        One step in the GA main algorithm
        1. Updating mating pool with current population
        2. Creating a new Generation
        """
        self.updateMatingPool()
        self.newGeneration()

    def search(self):
        """
        General search template.
        Iterates for a given number of steps
        """
        self.iteration = 0
        while self.iteration < self.maxIterations:
            self.GAStep()
            self.iteration += 1
            # print(self.iteration)

        print ("Total iterations: ",self.iteration)
        print ("Best Solution: ", self.best.getFitness())

        # Writing the results to the file
        file.write(f'Total iterations: {self.iteration}')
        file.write('\n')
        file.write(f'Best Solution: {self.best.getFitness()}')
        file.write('\n')
        file.write('====================================================== \n')

# if len(sys.argv) < 2:
#     print ("Error - Incorrect input")
#     print ("Expecting python BasicTSP.py [instance] ")
#     sys.exit(0)


# problem_file = sys.argv[1]
problem_file = "inst-0.tsp"

# ga = BasicTSP(problem_file, 300, 0.1, 500)
# ga = BasicTSP(problem_file, 100, 0.1, 500, 0, 0, 0, 0)   # Initial Random, Selection Random, Reciprocal = 1
# ga = BasicTSP(problem_file, 10, 0.1, 500, 0, 0, 0, 0)   # Initial Random, Selection Random, Inversion = 0
# ga = BasicTSP(problem_file, 10, 0.1, 500, 1, 0, 0, 1)   # Initial Heuristic, Selection Random, Reciprocal = 1
# ga = BasicTSP(problem_file, 10, 0.1, 500, 1, 0, 0, 0)   # Initial Heuristic, Selection Random, Inversion = 0


####TEST on inst-01#########
file = open('test_run.txt', 'a')


file.write(f'ga = BasicTSP({problem_file}, 100, 0.1, 500, 0, 0, 0, 0) => Configuration 1 \n')
ga = BasicTSP(problem_file, 100, 0.1, 500, 0, 0, 0, 0)
ga.search()

file.write(f'ga = BasicTSP({problem_file}, 100, 0.1, 500, 0, 0, 1, 1) => Configuration 2 \n')
ga = BasicTSP(problem_file, 100, 0.1, 500, 0, 0, 1, 1)
ga.search()

file.write(f'ga = BasicTSP({problem_file}, 100, 0.1, 500, 0, 1, 0, 1) => Configuration 3 \n')
ga = BasicTSP(problem_file, 100, 0.1, 500, 0, 1, 0, 1)
ga.search()

file.write(f'ga = BasicTSP({problem_file}, 100, 0.1, 500, 0, 1, 1, 1) => Configuration 4 \n')
ga = BasicTSP(problem_file, 100, 0.1, 500, 0, 1, 1, 1)
ga.search()


file.write(f'ga = BasicTSP({problem_file}, 100, 0.1, 500, 0, 1, 1, 0) => Configuration 5 \n')
ga = BasicTSP(problem_file, 100, 0.1, 500, 0, 1, 1, 0)
ga.search()

file.write(f'ga = BasicTSP({problem_file}, 100, 0.1, 500, 0, 1, 0, 0) => Configuration 6 \n')
ga = BasicTSP(problem_file, 100, 0.1, 500, 0, 1, 0, 0)
ga.search()

file.write(f'ga = BasicTSP({problem_file}, 100, 0.1, 500, 1, 1, 1, 1) => Configuration 7 \n')
ga = BasicTSP(problem_file, 100, 0.1, 500, 1, 1, 1, 1)
ga.search()

file.write(f'ga = BasicTSP({problem_file}, 100, 0.1, 500, 1, 1, 0, 0) => Configuration 8 \n')
ga = BasicTSP(problem_file, 100, 0.1, 500, 1, 1, 0, 0)
ga.search()

#
# file.write('ga = BasicTSP(problem_file, 100, 0.1, 200, 0, 1, 1, 1) \n')
# ga = BasicTSP(problem_file, 100, 0.1, 200, 0, 1, 1, 1)
# ga.search()
#
# file.write('ga = BasicTSP(problem_file, 100, 0.1, 200, 0, 0, 1, 0) \n')
# ga = BasicTSP(problem_file, 100, 0.1, 200, 0, 0, 1, 0)
# ga.search()
#
# file.write('ga = BasicTSP(problem_file, 100, 0.1, 200, 0, 0, 0, 1) \n')
# ga = BasicTSP(problem_file, 100, 0.1, 200, 0, 0, 0, 1)
# ga.search()
#
# file.write('ga = BasicTSP(problem_file, 100, 0.1, 200, 1, 1, 1, 0) \n')
# ga = BasicTSP(problem_file, 100, 0.1, 200, 1, 1, 1, 0)
# ga.search()
#
# file.write('ga = BasicTSP(problem_file, 100, 0.1, 200, 1, 1, 0, 1) \n')
# ga = BasicTSP(problem_file, 100, 0.1, 200, 1, 1, 0, 1)
# ga.search()
#
#
# file.write('ga = BasicTSP(problem_file, 100, 0.1, 200, 0, 1, 1, 0) \n')
# ga = BasicTSP(problem_file, 100, 0.1, 200, 0, 1, 1, 0)
# ga.search()
#
# file.write('ga = BasicTSP(problem_file, 100, 0.1, 200, 1, 0, 0, 1) \n')
# ga = BasicTSP(problem_file, 100, 0.1, 200, 1, 0, 0, 1)
# ga.search()
#
# file.write('ga = BasicTSP(problem_file, 100, 0.1, 200, 1, 0, 1, 0) \n')
# ga = BasicTSP(problem_file, 100, 0.1, 200, 1, 0, 1, 0)
# ga.search()
#
# file.write('ga = BasicTSP(problem_file, 100, 0.1, 200, 0, 1, 0, 1) \n')
# ga = BasicTSP(problem_file, 100, 0.1, 200, 0, 1, 0, 1)
# ga.search()

file.close()
'''
BasicTSP:
Parameter List:
1. Filename
2. Population Size
3. Mutation Rate
4. Maximum Iterations
5. Initial Solution = {0: Random, 1: Heuristic}
6. Selection/MatingPool = {0: Random, 1: Stochastic }
5. Crossover type = {0:Uniform Crossover, 1: PMX Crossover}
6. Mutation Type = {0: Inversion Exchange, 1: Reciprocal Exchange}
'''