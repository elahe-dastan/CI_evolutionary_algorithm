class Chromosome:
    def __init__(self, chromosome_length):
        self.chromosome_length = chromosome_length
        self.genes = self.random_chromosome()
        self.fitness = 0

    def random_chromosome(self):
        raise NotImplementedError
