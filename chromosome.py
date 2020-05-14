import numpy as np
from random import randint


class Chromosome:
    def __init__(self, chromosome_length):
        self.fitness = 0
        self.chromosome_length = chromosome_length
        self.genes = np.empty(chromosome_length, dtype=int)

    # representation of the knapsack problem
    def random_chromosome(self):
        for i in range(self.chromosome_length):
            self.genes[i] = randint(0, 1)
