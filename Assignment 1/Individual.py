

"""
Basic TSP Example
file: Individual.py
"""

import random
import math


class Individual:
    def __init__(self, _size, _data, _solution):
        """
        Parameters and general variables
        """
        self.fitness    = 0
        self.genes      = []
        self.genSize    = _size
        self.data       = _data
        self.solution   = _solution

        self.genes = list(self.data.keys())

        if self.solution == 0:
            for i in range(0, self.genSize):
                n1 = random.randint(0, self.genSize-1)
                n2 = random.randint(0, self.genSize-1)
                tmp = self.genes[n2]
                self.genes[n2] = self.genes[n1]
                self.genes[n1] = tmp

        elif self.solution == 1:
            # TODO : To create population with Heuristic approach
            tCost = 0

            n1 = random.randint(0, self.genSize - 1)  # Selecting the random index value from the genSize
            city_list = [self.genes[n1]]  # Creating the Starting Point for the Route
            del self.genes[n1]   # Removing the Element from the Chromosome

            current_city = city_list[0]  # Assigning the first selected city value to the current city

            while len(self.genes) > 0:
                next_city = self.genes[0]
                path_cost = self.euclideanDistance(current_city, next_city)
                gene_index = 0

                for city_index in range(1, len(self.genes)):
                    city = self.genes[city_index]
                    cost = self.euclideanDistance(current_city, city)
                    if path_cost > cost:
                        path_cost = cost
                        next_city = city
                        gene_index = city_index

                current_city = next_city
                city_list.append(current_city)
                del self.genes[gene_index]

            self.genes = city_list

    def setGene(self, genes):
        """
        Updating current choromosome
        """
        self.genes = []
        for gene_i in genes:
            self.genes.append(gene_i)

    def copy(self):
        """
        Creating a new individual
        """
        ind = Individual(self.genSize, self.data, 0)
        for i in range(0, self.genSize):
            ind.genes[i] = self.genes[i]
        ind.fitness = self.getFitness()
        return ind

    def euclideanDistance(self, c1, c2):
        """
        Distance between two cities
        """
        d1 = self.data[c1]
        d2 = self.data[c2]
        return math.sqrt( (d1[0]-d2[0])**2 + (d1[1]-d2[1])**2 )

    def getFitness(self):
        return self.fitness

    def computeFitness(self):
        """
        Computing the cost or fitness of the individual
        """
        self.fitness    = self.euclideanDistance(self.genes[0], self.genes[len(self.genes)-1])
        for i in range(0, self.genSize-1):
            self.fitness += self.euclideanDistance(self.genes[i], self.genes[i+1])

