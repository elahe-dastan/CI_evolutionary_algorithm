from evolutionary_algorithm import EvolutionaryAlgorithm


class Knapsack(EvolutionaryAlgorithm):
    def initial_population(self):
        for i in range(self.m):
            chromosome = BinaryChromosome(self.n)
            chromosome.random_chromosome()
            chromosome.fitness = self.calculate_fitness(chromosome)
            self.population[i] = chromosome
        self.log.append(self._save_current_log())
