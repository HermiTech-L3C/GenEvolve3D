# evolution.py

import random
import copy

class Gene:
    def __init__(self, source_type, source_num, sink_type, sink_num, weight):
        self.source_type, self.source_num = source_type, source_num
        self.sink_type, self.sink_num = sink_type, sink_num
        self.weight = weight
        self.source_pos = (
            random.uniform(-0.8, 0.8),
            random.uniform(-0.8, 0.8),
            random.uniform(-0.8, 0.8)
        )
        self.sink_pos = (
            random.uniform(-0.8, 0.8),
            random.uniform(-0.8, 0.8),
            random.uniform(-0.8, 0.8)
        )
        self.activity = abs(weight)

    def mutate(self):
        self.weight += random.uniform(-0.1, 0.1)
        self.activity = abs(self.weight)

class Genome:
    def __init__(self, genes=None):
        self.genes = genes if genes else []

    def add_connection(self, source_type, source_num, sink_type, sink_num, weight):
        self.genes.append(Gene(source_type, source_num, sink_type, sink_num, weight))

    def deep_copy(self):
        return copy.deepcopy(self)

class Individual:
    def __init__(self, genome):
        self.genome = genome
        self.fitness = 0

    def evaluate_fitness(self):
        self.fitness = random.uniform(0, 10)

    def mutate(self):
        if self.genome.genes:
            random.choice(self.genome.genes).mutate()

class Evolution:
    def __init__(self, population_size, mutation_rate=0.1):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.population = [Individual(self.random_genome()) for _ in range(population_size)]
        self.generation = 0
        self.average_fitness = 0

    def random_genome(self):
        return Genome([
            Gene('type1', 0, 'type2', 1, random.uniform(-1, 1))
            for _ in range(random.randint(1, 3))
        ])

    def run_generation(self):
        for ind in self.population:
            ind.evaluate_fitness()
        self.update_population()

    def update_population(self):
        self.population.sort(key=lambda ind: ind.fitness, reverse=True)
        self.population = self.population[:self.population_size // 2] + self.create_next_generation()
        self.generation += 1
        self.average_fitness = sum(ind.fitness for ind in self.population) / len(self.population)

    def create_next_generation(self):
        next_generation = []
        while len(next_generation) < self.population_size // 2:
            parent1, parent2 = random.sample(self.population, 2)
            child = Individual(self.crossover(parent1.genome, parent2.genome))
            if random.random() < self.mutation_rate:
                child.mutate()
            next_generation.append(child)
        return next_generation

    def crossover(self, genome1, genome2):
        gene_split = len(genome1.genes) // 2
        new_genes = (
            random.sample(genome1.genes, gene_split)
            + random.sample(genome2.genes, len(genome2.genes) - gene_split)
        )
        return Genome(new_genes)
