from evolutionary_algorithm import EvolutionaryAlgorithm
import numpy as np
import evolutionary_algorithms_functions as ea


class KnapSack(EvolutionaryAlgorithm):
    def __init__(self, file, m, y, representation, max_evaluation_count):
        stochastic_universal_sampling_parameters = {}
        q_tournament_selection_parameters = {"q": 2}
        super().__init__(m, y, representation, max_evaluation_count,
                         ea.stochastic_universal_sampling, stochastic_universal_sampling_parameters,
                         ea.q_tournament_selection, q_tournament_selection_parameters, ea.single_point_crossover)
        self.file = file
        self.max_weight = 0
        self.weights = []
        self.values = []

    def read_file(self):
        f = open(self.file, "r")
        arr = f.readline().split()
        self.chromosome_length = int(arr[0])
        self.max_weight = int(arr[1])

        self.weights = np.empty(self.chromosome_length, dtype=int)
        self.values = np.empty(self.chromosome_length, dtype=int)

        for i in range(self.chromosome_length):
            value_weight = f.readline().split()
            self.values[i] = int(value_weight[0])
            self.weights[i] = int(value_weight[1])

    def solve(self):
        self.read_file()
        self.initial_population()
        self.run("log.txt")

    def calculate_fitness(self, chromosome):
        chromosome_weight = 0
        chromosome_value = 0

        for i in range(self.chromosome_length):
            if chromosome.genes[i] == 1:
                chromosome_weight += self.weights[i]
                chromosome_value += self.values[i]

        fitness = chromosome_value

        if chromosome_weight > self.max_weight:
            fitness -= chromosome_weight - self.max_weight

        self.evaluation_counter += 1

        if fitness < 0:
            return 1 / abs(fitness)

        return fitness
