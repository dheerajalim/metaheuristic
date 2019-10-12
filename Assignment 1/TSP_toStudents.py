

"""
Author: Dheeraj Alimchandani
file: TSP_R00182505
Rename this file to TSP_x.py where x is your student number 
"""

import random
from Individual import *
import sys
import time
import itertools

myStudentNum = 'R00182505' # Replace 12345 with your student number
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
        Parameters for the all available methods
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
        """
        # TODO : To create population with Heuristic approach - Done
        for i in range(0, self.popSize):
            individual = Individual(self.genSize, self.data, self.initialSolution)
            individual.computeFitness()
            self.population.append(individual)

        self.best = self.population[0].copy()
        for ind_i in self.population:
            if self.best.getFitness() > ind_i.getFitness():
                self.best = ind_i.copy()
        print ("Best initial sol: ",self.best.getFitness())

        file.write(f'Best initial sol: {self.best.getFitness()}')
        file.write('\n')



    def updateBest(self, candidate):
        # print('Candidate Fitness = ',candidate.getFitness())
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
        Your stochastic universal sampling Selection Implementation
        """
        # TODO : Need to implement the Selection Probability to generate Mating Pool (Check: stochasticUniversalSampling)

        # Need to select two Parents
        N_parent = 2
        distance_pointers = 1/N_parent
        indA_pointer = random.uniform(0,distance_pointers)
        indB_pointer = indA_pointer + distance_pointers

        parent_test = True
        for ind,pointer in self.matingPool_sus.items():
            if parent_test:
                if indA_pointer < pointer:
                    parent_a = ind
                    parent_test = False
                    continue
            if indB_pointer < pointer:
                parent_b = ind
                break

        return [parent_a, parent_b]

    def uniformCrossover(self, indA, indB):
        """
        Your Uniform Crossover Implementation
        """
        # pos_list : Creating a list to contain the randomly selected locations that will not change.
        # Selecting 4 random locations
        pos_list = []
        for num in range(0, 4):
            pos_list.append(random.randint(0, self.genSize  - 1))

        # Initializing the offspring list with -1 in order to fill the changeable genes
        offspring_A = list(itertools.repeat(-1, self.genSize))
        offspring_B = list(itertools.repeat(-1, self.genSize))

        # Updating the offsprings with the genes that are non changeable
        for x in range(0, self.genSize):
            if x in pos_list:
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
        Your PMX Crossover Implementation
        """
        # print('Parent A = ', indA.genes)
        # print('Parent B = ', indB.genes)

        # Taking the random indexes to select genes that will reverse in the offspring
        indexB = random.randint(0, self.genSize - 1)
        indexA = random.randint(0, indexB)

        # print('Index A', indexA)
        # print('Index B', indexB)

        # Creating a mapping space for the reversed genes:
        self.map_indA = {}
        self.map_indB = {}

        # Creating the copy oof original Parent
        indA_orig = indA.copy()
        indB_orig = indB.copy()

        # The below is used to create the Mapping for the genes which were swapped in offsprings
        for x in range(indexA, indexB + 1):
            tmp = indA.genes[x]
            indA.genes[x] = indB.genes[x]
            indB.genes[x] = tmp
            self.map_indA[indA.genes[x]] = indB.genes[x]

        for key, value in self.map_indA.items():
            self.map_indB[value] = key

        # print('Parent A with Modification = ', indA.genes)
        # print('Parent B with Modification = ', indB.genes)

        # Replacing the genes with more than one occurrence to -1
        for i in range(0, self.genSize):
            if indexA <= i <= indexB:
                continue
            else:
                if indA.genes.count(indA.genes[i]) > 1:
                    indA.genes[i] = -1
                if indB.genes.count(indB.genes[i]) > 1:
                    indB.genes[i] = -1

        self.pmx_mapper(indA_orig, indA, 'A')
        self.pmx_mapper(indB_orig, indB, 'B')

        return indA, indB

        #
        #
        # print('MAp A', self.map_indA)
        # print('MAp B', self.map_indB)
        #
        # print('Offspring A = ', indA.genes)
        # print('Offspring B = ', indB.genes)
        # exit()

    def pmx_mapper(self,ind_orig, ind, parent):

        for x in range(0, self.genSize):
            mapping_loop = True
            if ind.genes[x] == -1:

                if parent == 'A':
                    mapper = self.map_indA[ind_orig.genes[x]]
                elif parent == 'B':
                    mapper = self.map_indB[ind_orig.genes[x]]

                while mapping_loop:
                    if mapper in ind.genes:
                        if parent == 'A':
                            mapper = self.map_indA[mapper]
                        elif parent == 'B':
                            mapper = self.map_indB[mapper]
                    else:
                        mapping_loop = False

                ind.genes[x] = mapper



    def reciprocalExchangeMutation(self, indA, indB):
        """
        Your Reciprocal Exchange Mutation implementation
        """
        # TODO : Implemnetation of Reciprocal Mutation - Done

        self.mutation(indA, indB)

    def inversionMutation(self, indA, indB):
        """
        Your Inversion Mutation implementation
        """
        # TODO : Implemnetation of Inversion Mutation - Done

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

    # This method is used to swap the values in the Reciprocal Mutation process for the Child
    def reciprocal_mutation_flip(self, ind, indexA, indexB):
        tmp = ind.genes[indexA]
        ind.genes[indexA] = ind.genes[indexB]
        ind.genes[indexB] = tmp
        ind.computeFitness()
        self.updateBest(ind)

    def updateMatingPool(self):
        """
        Updating the mating pool before creating a new generation
        """

        if self.selection == 0 :
            self.matingPool = []
            for ind_i in self.population:
                self.matingPool.append(ind_i.copy())

        elif self.selection == 1:
            # TODO : Create Mating Pool based on stochastic selection
            self.fitness_list = []
            self.minimize_fitness_list = []
            self.selection_probability_fitness_list = []
            for ind_i in self.population:
                self.fitness_list.append(ind_i.getFitness())

            max_fitness = max(self.fitness_list) + 1 # Adding 1 to avoid value to turn 0 on subtraction

            for fitness in self.fitness_list:
                self.minimize_fitness_list.append(max_fitness - fitness)

            fitness_sum = sum(self.minimize_fitness_list)

            for fitness in self.minimize_fitness_list:
                self.selection_probability_fitness_list.append(fitness/fitness_sum)

            # print(self.fitness_list)
            # print(self.minimize_fitness_list)
            # print(self.selection_probability_fitness_list)
            # print(max(self.selection_probability_fitness_list))

            ind_selection_range = []
            ind_selection_range.append(self.selection_probability_fitness_list[0])
            for fitness in range(1,len(self.selection_probability_fitness_list)):
                ind_selection_range.append(ind_selection_range[fitness-1] + self.selection_probability_fitness_list[fitness])

            # print(ind_selection_range)

            # Now we need to create a dictionary of mating pool with each individual and its selection probability

            for i in range(0,len(self.population)):
                self.matingPool_sus[self.population[i]] = ind_selection_range[i]


    def newGeneration(self):
        """
        Creating a new generation
        1. Selection
        2. Crossover
        3. Mutation
        """

        for i in range(0, len(self.population),2):
            """
            Depending of your experiment you need to use the most suitable algorithms for:
            1. Select two candidates
            2. Apply Crossover
            3. Apply Mutation
            """
            if self.selection == 0:
                partnerA, partnerB = self.randomSelection()

            elif self.selection == 1:
                partnerA, partnerB = self.stochasticUniversalSampling()

            ##Crossover
            if self.crossoverType == 0:
                # TODO : Uniform Crossover - Done
                start = time.time()
                child_a, child_b = self.uniformCrossover(partnerA, partnerB)
                # print('crossover', time.time() - start)


            elif self.crossoverType == 1:
                # TODO : PMX Crossover - Done
                start = time.time()
                child_a, child_b = self.pmxCrossover(partnerA, partnerB)
                # print('crossover', time.time() - start)

            # start = time.time()
            # child = self.crossover(partnerA, partnerB)
            # print('crossover', time.time() - start)

            ##Mutation
            # self.mutation(child)
            # self.reciprocalExchangeMutation(child)
            if self.mutationType == 0:
                start = time.time()
                self.inversionMutation(child_a, child_b)
                # print('Mutation', time.time() - start)

            elif self.mutationType == 1:
                start = time.time()
                self.reciprocalExchangeMutation(child_a, child_b)
                # print('Mutation', time.time() - start)

                # print('Mutation', time.time() - start)

            # self.inversionMutation(child)

            # Generation of new population by adding the child

            self.population[i] = child_a
            self.population[i+1] = child_b

    def GAStep(self):
        """
        One step in the GA main algorithm
        1. Updating mating pool with current population
        2. Creating a new Generation
        """

        self.updateMatingPool()
        start = time.time()
        self.newGeneration()
        end = time.time()
        # print('total = ', end-start)

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
problem_file = "inst-13.tsp"

# ga = BasicTSP(problem_file, 300, 0.1, 500)
# ga = BasicTSP(problem_file, 100, 0.1, 500, 0, 0, 0, 0)   # Initial Random, Selection Random, Reciprocal = 1
# ga = BasicTSP(problem_file, 10, 0.1, 500, 0, 0, 0, 0)   # Initial Random, Selection Random, Inversion = 0
# ga = BasicTSP(problem_file, 10, 0.1, 500, 1, 0, 0, 1)   # Initial Heuristic, Selection Random, Reciprocal = 1
# ga = BasicTSP(problem_file, 10, 0.1, 500, 1, 0, 0, 0)   # Initial Heuristic, Selection Random, Inversion = 0


####TEST on inst-01#########
file = open('test_run_test.txt', 'w')
file.write('ga = BasicTSP(problem_file, 100, 0.1, 500, 1, 0, 0, 0) \n')
ga = BasicTSP(problem_file, 100, 0.1, 500, 0, 1, 0, 0)
ga.search()

# file.write('ga = BasicTSP(problem_file, 100, 0.1, 200, 0, 0, 0, 0) \n')
# ga = BasicTSP(problem_file, 100, 0.1, 200, 0, 0, 0, 0)
# ga.search()

# file.write('ga = BasicTSP(problem_file, 100, 0.1, 200, 1, 0, 0, 0) \n')
# ga = BasicTSP(problem_file, 100, 0.1, 200, 1, 0, 0, 0)
# ga.search()
#
# file.write('ga = BasicTSP(problem_file, 100, 0.1, 200, 0, 1, 0, 0) \n')
# ga = BasicTSP(problem_file, 100, 0.1, 200, 0, 1, 0, 0)
# ga.search()
#
#
# file.write('ga = BasicTSP(problem_file, 100, 0.1, 200, 1, 1, 0, 0) \n')
# ga = BasicTSP(problem_file, 100, 0.1, 200, 1, 1, 0, 0)
# ga.search()
#
# file.write('ga = BasicTSP(problem_file, 100, 0.1, 200, 1, 1, 1, 1) \n')
# ga = BasicTSP(problem_file, 100, 0.1, 200, 1, 1, 1, 1)
# ga.search()
#
# file.write('ga = BasicTSP(problem_file, 100, 0.1, 200, 1, 0, 1, 1) \n')
# ga = BasicTSP(problem_file, 100, 0.1, 200, 1, 0, 1, 1)
# ga.search()
#
# file.write('ga = BasicTSP(problem_file, 100, 0.1, 200, 0, 0, 1, 1) \n')
# ga = BasicTSP(problem_file, 100, 0.1, 200, 0, 0, 1, 1)
# ga.search()
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