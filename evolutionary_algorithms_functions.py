from random import randint
import numpy as np


def binary_random_gene_generator(chromosome_length):
    genes = []
    for i in range(chromosome_length):
        genes.append(randint(0, 1))

    return genes


def permutation_random_gene_generator(chromosome_length):
    genes = np.arange(chromosome_length)
    np.random.shuffle(genes)

    return genes
