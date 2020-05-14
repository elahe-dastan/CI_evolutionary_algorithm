from chromosome import Chromosome
import numpy as np


class EvolutionaryAlgorithm:
    def __init__(self, m, n, y, weights, values, max_weight, total_value):
        # mu
        self.m = m
        # length of chromosome
        self.n = n
        self.y = y
        self.weights = weights
        self.values = values
        self.max_weight = max_weight
        self.total_value = total_value
        self.evaluation_counter = 0
        self.population = np.array(m, dtype=Chromosome)

    def initial_population(self):
        for i in range(self.m):
            chromosome = Chromosome(self.n)
            chromosome.random_chromosome()
            chromosome.fitness = self.calculate_fitness(chromosome)
            self.population[i] = chromosome

    def calculate_fitness(self, chromosome):
        chromosome_weight = 0
        chromosome_value = 0

        for i in range(self.n):
            if chromosome.genes[i] == 1:
                chromosome_weight += self.weights[i]
                chromosome_value += self.values[i]

        fitness = 0
        if chromosome_weight > self.max_weight:
            fitness += 10 * (chromosome_weight - self.max_weight)

        if chromosome_value < self.total_value:
            fitness += self.total_value - chromosome_value

        self.evaluation_counter += 1

        return fitness

    def parent_selection(self):
        total_fitness = 0
        for i in range(self.m):
            total_fitness += self.population[i].fitness

        probs = np.empty(self.m, dtype=float)

        for i in range(self.m):
            probs[i] = self.population[i].fitness / total_fitness

        return self.stochastic_universal_sampling(probs)

    def stochastic_universal_sampling(self, probs):
        index = np.arange(self.m)
        np.random.shuffle(index)
        items = self.population[index]
        probs = probs[index]
        start_index = np.random.uniform(0, 1 / self.y, 1)
        index_of_choose = np.linspace(start_index, 1, self.y)
        cum_sum = np.cumsum(probs)
        selected_items = []
        items_pointer = 0

        for choice in index_of_choose:
            while cum_sum[items_pointer] < choice:
                items_pointer += 1
            selected_items.append(items[items_pointer])

        return np.array(selected_items)
