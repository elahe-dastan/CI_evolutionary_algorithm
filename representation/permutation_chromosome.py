from representation.chromosome import Chromosome
import numpy as np


class PermutationChromosome(Chromosome):
    def random_chromosome(self):
        genes = np.arange(self.chromosome_length)
        np.random.shuffle(genes)

        return genes
