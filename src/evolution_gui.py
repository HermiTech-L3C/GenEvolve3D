import random
import pythreejs as three
from evolution import Gene, Genome, Individual, Position

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

    # Visualization methods
    def draw_gene_network(self):
        for gene in self.population[0].genome.genes:
            self.draw_node(gene.source_pos, gene.activity)
            self.draw_node(gene.sink_pos, gene.activity)
            self.draw_connection(gene.source_pos, gene.sink_pos)

    def draw_node(self, position, activity):
        # Improved node visualization
        color = 'red' if activity > 0.5 else 'green'
        geometry = three.SphereBufferGeometry(radius=activity * 0.1, widthSegments=32, heightSegments=32)
        material = three.MeshBasicMaterial(color=color)
        sphere = three.Mesh(geometry=geometry, material=material)
        sphere.position = [position.x, position.y, position.z]
        self.scene.add(sphere)

    def draw_connection(self, source_pos, sink_pos):
        # Improved connection visualization
        color = 'blue' if abs(source_pos.x - sink_pos.x) > 0.5 else 'yellow'
        line = three.Line(
            geometry=three.BufferGeometry(attributes={
                "position": three.BufferAttribute(array=[[source_pos.x, source_pos.y, source_pos.z], [sink_pos.x, sink_pos.y, sink_pos.z]], itemSize=3),
            }),
            material=three.LineBasicMaterial(color=color)
        )
        self.scene.add(line)

    # Running the visualization
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

