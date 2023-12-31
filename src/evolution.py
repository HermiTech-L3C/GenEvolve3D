from collections import namedtuple
import random

Position = namedtuple('Position', ['x', 'y', 'z'])
Gene = namedtuple('Gene', ['source_type', 'source_num', 'sink_type', 'sink_num', 'weight', 'source_pos', 'sink_pos', 'activity'])
Genome = namedtuple('Genome', ['genes'])

class Individual:
    def __init__(self, genome):
        self.genome = genome
        self.fitness = 0

    def evaluate_fitness(self, fitness_function):
        self.fitness = fitness_function(self.genome)

    def mutate(self, mutation_strength=0.1):
        if self.genome.genes:
            gene_to_mutate = random.choice(self.genome.genes)
            gene_to_mutate = gene_to_mutate._replace(weight=gene_to_mutate.weight + random.uniform(-mutation_strength, mutation_strength),
                                                     activity=abs(gene_to_mutate.weight))

class Evolution:
    def __init__(self, population_size, mutation_rate=0.1, fitness_function=None):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.fitness_function = fitness_function or (lambda genome: random.uniform(0, 10))
        self.population = [Individual(self._random_genome()) for _ in range(population_size)]
        self.generation = 0
        self.average_fitness = 0

    def _random_genome(self):
        return Genome([self._random_gene() for _ in range(random.randint(*self._genes_range))])

    def _random_gene(self):
        return Gene(
            random.choice(self._source_types),
            0,
            random.choice(self._sink_types),
            1,
            random.uniform(*self._weight_range),
            Position(*[random.uniform(-0.8, 0.8) for _ in range(3)]),
            Position(*[random.uniform(-0.8, 0.8) for _ in range(3)]),
            0  # Initial activity
        )

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
            child_genome = self._crossover(parent1.genome, parent2.genome)
            for gene in child_genome.genes:
                if random.random() < self.mutation_rate:
                    gene.mutate()
            next_generation.append(Individual(child_genome))
        return next_generation

    def _crossover(self, genome1, genome2):
        gene_split = len(genome1.genes) // 2
        new_genes = random.sample(genome1.genes, gene_split) + random.sample(genome2.genes, len(genome2.genes) - gene_split)
        return Genome(new_genes)

    _source_types = ['type1', 'type2']
    _sink_types = ['type2', 'type3']
    _weight_range = (-1, 1)
    _genes_range = (1, 3)

# Example Usage
evolution_instance = Evolution(population_size=10, mutation_rate=0.1)
evolution_instance.run_generation()