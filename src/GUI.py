import random
import copy
import tkinter as tk
from mayavi import mlab
from traits.api import HasTraits, Instance
from traitsui.api import View, Item
from mayavi.core.ui.api import MlabSceneModel, SceneEditor

# Constants for Mayavi visualization
SCREEN_DIMENSIONS = (800, 600)
PERSPECTIVE_SETTINGS = (45, 1, 0.1, 50.0)
TRANSLATION_SETTINGS = (0, 0, -5)
BORDER_MARGIN = 50  # Margin for the border

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

class EvolutionGUI(HasTraits):
    evolution = Instance(Evolution)
    scene = Instance(MlabSceneModel, ())

    def __init__(self, evolution):
        super().__init__(evolution=evolution)
        self.create_widgets()

    def create_widgets(self):
        self.start_button = tk.Button(text="Start Evolution", command=self.start_evolution)
        self.start_button.pack()

        self.stop_button = tk.Button(text="Stop Evolution", command=self.stop_evolution, state=tk.DISABLED)
        self.stop_button.pack()

        self.mutation_scale = tk.Scale(from_=0, to=0.2, resolution=0.01, orient=tk.HORIZONTAL, label="Mutation Rate")
        self.mutation_scale.set(self.evolution.mutation_rate)
        self.mutation_scale.pack()

        self.status_label = tk.Label(text="Generation: 0\nAverage Fitness: 0.0")
        self.status_label.pack()

        # Create Mayavi scene editor
        self.view = View(Item('scene', editor=SceneEditor(scene_class=MayaviScene), height=500, width=600, show_label=False))

    def start_evolution(self):
        self.evolution.mutation_rate = self.mutation_scale.get()
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.update_status()

    def stop_evolution(self):
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def update_status(self):
        if self.evolution.generation < 100:  # Adjust the number of generations to visualize
            self.evolution.run_generation()
            self.scene.mlab.clf()
            self.draw_gene_network()
            gen, avg_fit = self.evolution.generation, self.evolution.average_fitness
            self.status_label.config(text=f"Generation: {gen}\nAverage Fitness: {avg_fit:.2f}")
            self.scene.mlab.view(azimuth=0, elevation=90)
            self.scene.mlab.draw()
            self.scene.mlab.savefig(f'generation_{gen}.png')
            self.scene.mlab.show()
            self.scene.mlab.save_camera('camera.npy')
            self.evolution.generation += 1

    def draw_gene_network(self):
        for gene in self.evolution.population[0].genome.genes:
            self.draw_node(gene.source_pos, gene.activity)
            self.draw_node(gene.sink_pos, gene.activity)
            self.draw_connection(gene.source_pos, gene.sink_pos)

    def draw_node(self, position, activity):
        mlab.points3d(position[0], position[1], position[2], activity, scale_factor=0.05 * activity, color=(1, 0, 0))

    def draw_connection(self, source_pos, sink_pos):
        x = [source_pos[0], sink_pos[0]]
        y = [source_pos[1], sink_pos[1]]
        z = [source_pos[2], sink_pos[2]]
        mlab.plot3d(x, y, z, color=(0, 0, 1), tube_radius=0.01)

    def run(self):
        self.edit_traits(view=self.view)

if __name__ == '__main__':
    evolution = Evolution(population_size=100)
    gui = EvolutionGUI(evolution)
    gui.configure_traits()
