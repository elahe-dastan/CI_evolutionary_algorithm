from representation.chromosome import Chromosome
from random import randint


class BinaryChromosome(Chromosome):
    # representation of the knapsack problem
    def random_chromosome(self):
        genes = []
        for i in range(self.chromosome_length):
            genes.append(randint(0, 1))

        return genes
