import evolutionary_algorithms_functions as ea
from city import City
from problems.knapsack import  KnapSack

k = KnapSack("knapsack_1.txt", 10, 20, ea.binary_random_gene_generator, 50000)
k.solve()

f = open("tsp_data.txt", "r")

cities = []
for i in range(194):
    coordinate = f.readline().split()
    identifier = int(coordinate[0])
    x = float(coordinate[1])
    y = float(coordinate[2])
    city = City(identifier, x, y)
    cities.append(city)

# EA_tsp = EvolutionaryAlgorithm(10, chromosome_length, ea.permutation_random_gene_generator, 20, 50000, weights,
#                                values, max_weight)
# EA_knapsack.initial_population()
#
# EA_knapsack.run("log.txt")
