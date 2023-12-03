import random
import copy
import threading
import time
import tkinter as tk
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Constants for OpenGL
SCREEN_DIMENSIONS = (800, 600)
PERSPECTIVE_SETTINGS = (45, 1, 0.1, 50.0)
TRANSLATION_SETTINGS = (0, 0, -5)
BORDER_MARGIN = 50  # Margin for the border

# Evolutionary Algorithm Classes
class Gene:
    def __init__(self, source_type, source_num, sink_type, sink_num, weight):
        self.source_type, self.source_num = source_type, source_num
        self.sink_type, self.sink_num = sink_type, sink_num
        self.weight = weight
        self.source_pos, self.sink_pos = self.random_position(), self.random_position()
        self.activity = 0

    @staticmethod
    def random_position():
        return (random.uniform(-0.8, 0.8), random.uniform(-0.8, 0.8), random.uniform(-0.8, 0.8))

    def mutate(self):
        self.weight += random.uniform(-0.1, 0.1)
        self.update_activity()

    def update_activity(self):
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
        return Genome([Gene('type1', 0, 'type2', 1, random.uniform(-1, 1)) for _ in range(random.randint(1, 3))])

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
        new_genes = random.sample(genome1.genes, gene_split) + random.sample(genome2.genes, len(genome2.genes) - gene_split)
        return Genome(new_genes)

# OpenGL-based Visualization
class OpenGLWidget:
    def __init__(self, evolution):
        self.evolution = evolution
        self.continue_running = True
        self.initialized = False

    def init_gl(self):
        pygame.init()
        pygame.display.set_mode(SCREEN_DIMENSIONS, DOUBLEBUF | OPENGL)
        gluPerspective(*PERSPECTIVE_SETTINGS)
        glTranslatef(*TRANSLATION_SETTINGS)
        self.initialized = True

    def run_evolution(self):
        if not self.initialized:
            self.init_gl()

        while self.continue_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stop()

            if self.evolution.population:
                self.evolution.run_generation()

            self.draw_gene_network()
            pygame.display.flip()
            time.sleep(0.5)  # Slower frame rate

    def draw_gene_network(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glViewport(BORDER_MARGIN, BORDER_MARGIN, SCREEN_DIMENSIONS[0] - 2 * BORDER_MARGIN, SCREEN_DIMENSIONS[1] - 2 * BORDER_MARGIN)

        for gene in self.evolution.population[0].genome.genes:
            self.draw_node(gene.source_pos, gene.activity)
            self.draw_node(gene.sink_pos, gene.activity)
            self.draw_connection(gene.source_pos, gene.sink_pos)

    def draw_node(self, position, activity):
        glPushMatrix()
        glTranslate(*position)
        glColor3f(*self.get_color_for_activity(activity))
        glutSolidSphere(activity * 0.05, 20, 20)  # Node size based on activity
        glPopMatrix()

    def draw_connection(self, source_pos, sink_pos):
        glColor3f(1, 1, 1)  # White color for connections
        glBegin(GL_LINES)
        glVertex3fv(source_pos)
        glVertex3fv(sink_pos)
        glEnd()

    def get_color_for_activity(self, activity):
        r = min(activity, 1)
        g = 1 - min(activity, 1)
        b = activity / 2  # Example color logic
        return r, g, b

    def stop(self):
        self.continue_running = False
        pygame.quit()

# Tkinter-based GUI
class EvolutionGUI:
    def __init__(self, evolution, opengl_widget):
        self.evolution = evolution
        self.opengl_widget = opengl_widget
        self.root = tk.Tk()
        self.root.title("Evolution Simulation")
        self.create_widgets()

    def create_widgets(self):
        self.start_button = tk.Button(self.root, text="Start Evolution", command=self.start_evolution)
        self.start_button.pack()

        self.stop_button = tk.Button(self.root, text="Stop Evolution", command=self.stop_evolution, state=tk.DISABLED)
        self.stop_button.pack()

        self.mutation_scale = tk.Scale(self.root, from_=0, to=0.2, resolution=0.01, orient=tk.HORIZONTAL, label="Mutation Rate")
        self.mutation_scale.set(self.evolution.mutation_rate)
        self.mutation_scale.pack()

        self.status_label = tk.Label(self.root, text="Generation: 0\nAverage Fitness: 0.0")
        self.status_label.pack()

    def start_evolution(self):
        self.evolution.mutation_rate = self.mutation_scale.get()
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        threading.Thread(target=self.opengl_widget.run_evolution).start()
        self.update_status()

    def stop_evolution(self):
        self.opengl_widget.stop()
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def update_status(self):
        if self.opengl_widget.continue_running:
            gen, avg_fit = self.evolution.generation, self.evolution.average_fitness
            self.status_label.config(text=f"Generation: {gen}\nAverage Fitness: {avg_fit:.2f}")
            self.root.after(500, self.update_status)

    def run(self):
        self.root.mainloop()

# Main function
def main():
    evolution = Evolution(population_size=100)
    opengl_widget = OpenGLWidget(evolution)
    gui = EvolutionGUI(evolution, opengl_widget)
    gui.run()

if __name__ == '__main__':
    main()
