import numpy as np


class Chromosome:
    def __init__(self, chromosome_length):
        self.chromosome_length = chromosome_length
        self.genes = np.empty(chromosome_length)
        self.fitness = 0

    def random(self, gene_generator):
        self.genes = gene_generator(self.chromosome_length)
