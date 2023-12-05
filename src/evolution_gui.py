import random
import pythreejs as three

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

    def mutate(self):
        self.weight += random.uniform(-0.1, 0.1)
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

    def evaluate_fitness(self):
        self.fitness = random.uniform(0, 10)

    def mutate(self):
        if self.genome.genes:
            gene_to_mutate = random.choice(self.genome.genes)
            gene_to_mutate.mutate()

class EvolutionPyThreejs:
    def __init__(self, population_size, mutation_rate=0.1):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.population = [Individual(self._random_genome()) for _ in range(population_size)]
        self.generation = 0
        self.average_fitness = 0
        self.scene = three.Scene()
        self.camera = three.PerspectiveCamera(position=[0, 0, 5], aspect=1)
        self.renderer = three.Renderer(scene=self.scene, camera=self.camera, controls=[three.OrbitControls(self.camera)])
        self.renderer.width = 800
        self.renderer.height = 600
        self.renderer.auto_clear = False
        self.controls = three.OrbitControls(self.camera)

    def _random_genome(self):
        return Genome([Gene('type1', 0, 'type2', 1, random.uniform(-1, 1)) for _ in range(random.randint(1, 3))])

    def run_generation(self):
        for individual in self.population:
            individual.evaluate_fitness()
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

    def draw_gene_network(self):
        for gene in self.population[0].genome.genes:
            self.draw_node(gene.source_pos, gene.activity)
            self.draw_node(gene.sink_pos, gene.activity)
            self.draw_connection(gene.source_pos, gene.sink_pos)

    def draw_node(self, position, activity):
        geometry = three.SphereBufferGeometry(radius=activity * 0.1, widthSegments=32, heightSegments=32)
        material = three.MeshBasicMaterial(color='red')
        sphere = three.Mesh(geometry=geometry, material=material)
        sphere.position = position
        self.scene.add(sphere)

    def draw_connection(self, source_pos, sink_pos):
        line = three.Line(
            geometry=three.BufferGeometry(attributes={
                "position": three.BufferAttribute(array=[source_pos, sink_pos], itemSize=3),
            }),
            material=three.LineBasicMaterial(color='blue')
        )
        self.scene.add(line)

    def run(self):
        self.controls.autoRotate = True
        self.controls.autoRotateSpeed = 3.0
        self.controls.enableDamping = True
        self.controls.dampingFactor = 0.2
        self.controls.rotateSpeed = 0.5
        self.controls.zoomSpeed = 1.2
        self.controls.addEventListener('change', self.render)

        self.render()
        self.controls.update()
        self.renderer

    def render(self):
        self.renderer.render(self.scene, self.camera)
