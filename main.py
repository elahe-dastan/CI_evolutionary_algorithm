import chromosome
import numpy as np
from evolutionary_algorithm import EvolutionaryAlgorithm

f = open("knapsack_1.txt", "r")
arr = f.readline().split()
chromosome_length = int(arr[0])
max_weight = int(arr[1])

weights = np.empty(chromosome_length, dtype=int)
values = np.empty(chromosome_length, dtype=int)
total_value = 0

for i in range(chromosome_length):
    value_weight = f.readline().split()
    values[i] = int(value_weight[0])
    total_value += values[i]
    weights[i] = int(value_weight[1])

EA = EvolutionaryAlgorithm(10, chromosome_length, 20, 1000, weights, values, max_weight, total_value)
EA.initial_population()

EA.run()

ch = chromosome.Chromosome()
print(ch.random_chromosome(10))

