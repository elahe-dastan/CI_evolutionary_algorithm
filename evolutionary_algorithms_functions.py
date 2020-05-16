from random import randint
import numpy as np
import warnings
import math
from random import randint
from representation.chromosome import Chromosome

def warning_data_type_check_selection_algorithms(items, probs):
    if type(items) == list:
        items = np.array(items)
    if type(probs) == list:
        probs = np.array(probs)
    if len(probs) != len(items):
        raise ValueError(
            "Length of probs and items must be equal! probs length = {} and items length = {}".format(
                len(probs), len(items)
            )
        )
    if type(probs) != np.ndarray or type(items) != np.ndarray:
        raise ValueError(
            "Type of items and probs must be list or np.array, items type = {} and probs type = {}".format(
                type(items), type(probs)
            )
        )
    if np.min(probs) < 0:
        raise ValueError("Probabilities can not contain negative values")

    if not math.isclose(np.sum(probs), 1):
        warnings.warn(
            "Sum of Probabilities array must be 1 but it is = {}, and we normalize it to reach sum equal 1".format(
                np.sum(probs)
            ),
            stacklevel=4,
        )
        probs = probs / np.sum(probs)
    return items, probs


# Representation
def binary_random_gene_generator(chromosome_length):
    genes = []
    for i in range(chromosome_length):
        genes.append(randint(0, 1))

    return genes


def permutation_random_gene_generator(chromosome_length):
    genes = np.arange(chromosome_length)
    np.random.shuffle(genes)

    return genes


# Selection
# I have to change it to linear ...
def stochastic_universal_sampling(population, probs, n, parameters):
    index = np.arange(len(population))
    np.random.shuffle(index)
    items = population[index]
    probs = probs[index]
    start_index = np.random.uniform(0, 1 / n, 1)
    index_of_choose = np.linspace(start_index, 1, n)
    cum_sum = np.cumsum(probs)
    selected_items = []
    items_pointer = 0

    for choice in index_of_choose:
        while cum_sum[items_pointer] < choice:
            if items_pointer == len(population) - 1:
                break
            items_pointer += 1

        selected_items.append(items[items_pointer])

    return np.array(selected_items)


def q_tournament_selection(items, probs, n, parameters):
    q = parameters['q']
    if n == 0:
        return np.array([])

    else:
        items, probs = warning_data_type_check_selection_algorithms(items, probs)
        index = np.arange(len(items))
        np.random.shuffle(index)
        items = items[index]
        probs = probs[index]

        selected_items = []
        len_items = len(items)

        for i in range(n):
            indexes = np.random.choice(np.arange(len_items), q, replace=False)
            selected_items.append(items[indexes[np.argmax(probs[indexes])]])

    return np.array(selected_items)


# Cross over
# probability
def single_point_crossover(parent1, parent2):
    idx = randint(1, parent1.chromosome_length - 1)
    chromosome1, chromosome2 = Chromosome(parent1.chromosome_length), Chromosome(parent1.chromosome_length)
    # rand = np.random.random()
    chromosome1.genes[:idx] = parent1.genes[:idx]
    chromosome1.genes[idx:] = parent2.genes[idx:]
    chromosome2.genes[:idx] = parent2.genes[:idx]
    chromosome2.genes[idx:] = parent1.genes[idx:]

    return chromosome1, chromosome2
