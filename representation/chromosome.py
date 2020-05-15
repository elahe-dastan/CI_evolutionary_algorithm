class Chromosome:
    def __init__(self, chromosome_length, gene_generator):
        self.chromosome_length = chromosome_length
        self.genes = gene_generator(chromosome_length)
        self.fitness = 0
