from representation.chromosome import *
import numpy as np
import random

import evolutionary_algorithms_functions as ea


# lamba = mu * 7


class EvolutionaryAlgorithm:
    def __init__(
            self, m, y, representation, max_evaluation_count,
            parent_selection_algo, parent_selection_algo_parameters,
            remaining_population_selection_algo, remaining_population_selection_algo_parameters, cross_over
    ):
        # mu
        self.m = m
        # length of chromosome
        self.chromosome_length = 0
        self.gene_generator = representation
        self.y = y
        self.max_evaluation_count = max_evaluation_count
        self.evaluation_counter = 0
        self.population = np.empty(m, dtype=Chromosome)
        self.log = []
        self.best_chromosome_fitness_in_total = 0
        self.generation_counter = 0
        self.parent_selection_algo = parent_selection_algo
        self.parent_selection_algo_parameters = parent_selection_algo_parameters
        self.remaining_population_selection_algo = remaining_population_selection_algo
        self.remaining_population_selection_algo_parameters = remaining_population_selection_algo_parameters
        self.cross_over = cross_over

    def run(self, save_log_path):
        while True:
            parents = self.parent_selection()
            children = self.new_children(parents)
            self.population = self.remaining_population_selection(
                self.population, children
            )
            self.generation_counter += 1
            self.log.append(self._save_current_log())

            if self.stop_condition():
                break
        with open(save_log_path, 'w') as file:
            for l in self.log:
                print(l, file=file)

        self.get_answer()

    def initial_population(self):
        for i in range(self.m):
            chromosome = Chromosome(self.chromosome_length)
            chromosome.random(self.gene_generator)
            chromosome.fitness = self.calculate_fitness(chromosome)
            self.population[i] = chromosome
        self.log.append(self._save_current_log())

    def calculate_fitness(self, chromosome):
        raise NotImplementedError

    def parent_selection(self):
        fitness_arr = np.array([x.fitness for x in self.population])
        probs = fitness_arr / np.sum(fitness_arr)

        return self.parent_selection_algo(self.population, probs, self.y, self.parent_selection_algo_parameters)

    def new_children(self, parents):
        children = []
        random.shuffle(parents)
        total_fitness = 0
        for i in range(0, len(parents) - 1, 2):
            chromosome1, chromosome2 = self.cross_over(parents[i], parents[i + 1])
            self.mutation(chromosome1, 0.1)
            self.mutation(chromosome2, 0.1)
            chromosome1.fitness = self.calculate_fitness(chromosome1)
            chromosome2.fitness = self.calculate_fitness(chromosome2)
            children += [chromosome1, chromosome2]
            if len(children) >= self.y:
                break

        return children[: self.y]

    def mutation(self, chromosome, prob):
        for i in range(self.chromosome_length):
            rand = np.random.random()
            if rand < prob:
                chromosome.genes[i] = int(not chromosome.genes[i])

    def remaining_population_selection(self, previous_population, children):
        items = np.concatenate((previous_population, children))
        fitness_arr = np.array([x.fitness for x in items])
        probs = fitness_arr / np.sum(fitness_arr)

        return self.remaining_population_selection_algo(items, probs, self.m, self.remaining_population_selection_algo_parameters)

    def stop_condition(self):
        return self.evaluation_counter > self.max_evaluation_count

    def _save_current_log(self):
        fitness = []
        best_phenotype_index = 0
        for i in range(1, len(self.population)):
            if self.population[i].fitness > self.population[best_phenotype_index].fitness:
                best_phenotype_index = i
            fitness.append(self.population[i].fitness)
        var_fitness = np.var(fitness)
        avg_fitness = np.average(fitness)
        if self.population[best_phenotype_index].fitness >= self.best_chromosome_fitness_in_total:
            self.best_chromosome_fitness_in_total = self.population[best_phenotype_index].fitness
            best_chrom = self.population[best_phenotype_index]
        return {'generation': self.generation_counter,
                'avg_fitness': avg_fitness,
                'var_fitness': var_fitness,
                # 'best_phenotype': best_chrom,
                'best_fitness': self.population[best_phenotype_index].fitness,
                }

    def get_answer(self):
        best_phenotype_index = 0
        for i in range(1, len(self.population)):
            if self.population[i].fitness > self.population[best_phenotype_index].fitness:
                best_phenotype_index = i

        chromosome_weight = 0
        chromosome_value = 0

        for i in range(self.chromosome_length):
            if self.population[best_phenotype_index].genes[i] == 1:
                chromosome_weight += self.weights[i]
                chromosome_value += self.values[i]

        print(chromosome_weight, chromosome_value)
