import numpy as np
from evolutionary_algorithm import EvolutionaryAlgorithm
from city import City

f = open("knapsack_1.txt", "r")
arr = f.readline().split()
chromosome_length = int(arr[0])
max_weight = int(arr[1])

weights = np.empty(chromosome_length, dtype=int)
values = np.empty(chromosome_length, dtype=int)

for i in range(chromosome_length):
    value_weight = f.readline().split()
    values[i] = int(value_weight[0])
    weights[i] = int(value_weight[1])

EA_knapsack = EvolutionaryAlgorithm(10, chromosome_length, 20, 50000, weights, values, max_weight)
EA_knapsack.initial_population()

EA_knapsack.run("log.txt")


f = open("tsp_data.txt", "r")

cities = []
for i in range(194):
    coordinate = f.readline().split()
    identifier = int(coordinate[0])
    x = float(coordinate[1])
    y = float(coordinate[2])
    city = City(identifier, x, y)
    cities.append(city)

# EA_tsp = EvolutionaryAlgorithm(10, chromosome_length, 20, 50000, weights, values, max_weight)
# EA_knapsack.initial_population()
#
# EA_knapsack.run("log.txt")
