import random
import copy

class Position:
    def __init__(self):
        self.x = random.uniform(-0.8, 0.8)
        self.y = random.uniform(-0.8, 0.8)
        self.z = random.uniform(-0.8, 0.8)

class Gene:
    def __init__(self, source_type, source_num, sink_type, sink_num, weight):
        self.source_type = source_type
        self.source_num = source_num
        self.sink_type = sink_type
        self.sink_num = sink_num
        self.weight = weight
        self.source_pos = Position()
        self.sink_pos = Position()
        self.activity = abs(weight)

    def mutate(self, mutation_strength=0.1):
        self.weight += random.uniform(-mutation_strength, mutation_strength)
        self.activity = abs(self.weight)

class Genome:
    def __init__(self, genes=None):
        self.genes = genes if genes is not None else []

    def add_connection(self, source_type, source_num, sink_type, sink_num, weight):
        new_gene = Gene(source_type, source_num, sink_type, sink_num, weight)
        self.genes.append(new_gene)

    def deep_copy(self):
        return copy.deepcopy(self)

class Individual:
    def __init__(self, genome):
        self.genome = genome
        self.fitness = 0

    def evaluate_fitness(self, fitness_function):
        self.fitness = fitness_function(self.genome)

    def mutate(self, mutation_strength=0.1):
        if self.genome.genes:
            gene_to_mutate = random.choice(self.genome.genes)
            gene_to_mutate.mutate(mutation_strength)

class Evolution:
    def __init__(self, population_size, mutation_rate=0.1, fitness_function=None):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.fitness_function = fitness_function or (lambda genome: random.uniform(0, 10))
        self.population = [Individual(self._random_genome()) for _ in range(population_size)]
        self.generation = 0
        self.average_fitness = 0

    def _random_genome(self):
        return Genome([Gene('type1', 0, 'type2', 1, random.uniform(-1, 1)) for _ in range(random.randint(1, 3))])

    def run_generation(self):
        for individual in self.population:
            individual.evaluate_fitness(self.fitness_function)
        self._update_population()

    def _update_population(self):
        self.population.sort(key=lambda individual: individual.fitness, reverse=True)
        self.population = self.population[:self.population_size // 2] + self._create_next_generation()
        self.generation += 1
        self.average_fitness = sum(individual.fitness for individual in self.population) / len(self.population)

    def _create_next_generation(self):
        next_generation = []
        while len(next_generation) < self.population_size // 2:
            parent1, parent2 = random.sample(self.population, 2)
            child = Individual(self._crossover(parent1.genome, parent2.genome))
            if random.random() < self.mutation_rate:
                child.mutate()
            next_generation.append(child)
        return next_generation

    def _crossover(self, genome1, genome2):
        gene_split = len(genome1.genes) // 2
        new_genes = random.sample(genome1.genes, gene_split) + random.sample(genome2.genes, len(genome2.genes) - gene_split)
        return Genome(new_genes)
