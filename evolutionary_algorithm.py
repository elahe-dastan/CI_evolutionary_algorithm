from representation.chromosome import *
import numpy as np
import random
import warnings
import math
import evolutionary_algorithms_functions as ea


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


class EvolutionaryAlgorithm:
    def __init__(
            self, m, n, y, max_evaluation_count, weights, values, max_weight
    ):
        # mu
        self.m = m
        # length of chromosome
        self.n = n
        self.y = y
        self.max_evaluation_count = max_evaluation_count
        self.weights = weights
        self.values = values
        self.max_weight = max_weight
        self.evaluation_counter = 0
        self.population = np.empty(m, dtype=Chromosome)
        self.log = []
        self.best_chromosome_fitness_in_total = 0
        self.generation_counter = 0

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
            chromosome = Chromosome(self.n, ea.binary_random_gene_generator)
            chromosome.fitness = self.calculate_fitness(chromosome)
            self.population[i] = chromosome
        self.log.append(self._save_current_log())


    def calculate_fitness(self, chromosome):
        chromosome_weight = 0
        chromosome_value = 0

        for i in range(self.n):
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

    def parent_selection(self):
        fitness_arr = np.array([x.fitness for x in self.population])
        probs = fitness_arr / np.sum(fitness_arr)

        return self.stochastic_universal_sampling(probs)

    # I have to change it to linear ...
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
                if items_pointer == self.m - 1:
                    break
                items_pointer += 1

            selected_items.append(items[items_pointer])

        return np.array(selected_items)

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

    def cross_over(self, parent1, parent2):
        idx = int(self.n / 2)
        chromosome1, chromosome2 = Chromosome(self.n, ea.binary_random_gene_generator), Chromosome(self.n, ea.binary_random_gene_generator)
        # rand = np.random.random()
        chromosome1.genes[:idx] = parent1.genes[:idx]
        chromosome1.genes[idx:] = parent2.genes[idx:]
        chromosome2.genes[:idx] = parent2.genes[:idx]
        chromosome2.genes[idx:] = parent1.genes[idx:]

        return chromosome1, chromosome2

    def mutation(self, chromosome, prob):
        for i in range(self.n):
            rand = np.random.random()
            if rand < prob:
                chromosome.genes[i] = int(not chromosome.genes[i])

    def remaining_population_selection(self, previous_population, children):
        items = np.concatenate((previous_population, children))
        fitness_arr = np.array([x.fitness for x in items])
        probs = fitness_arr / np.sum(fitness_arr)

        return self.q_tournament_selection(items, probs, 2, self.m)

    def q_tournament_selection(self, items, probs, q, n):
        # assert q != 0

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

        for i in range(self.n):
            if self.population[best_phenotype_index].genes[i] == 1:
                chromosome_weight += self.weights[i]
                chromosome_value += self.values[i]

        print(chromosome_weight, chromosome_value)
