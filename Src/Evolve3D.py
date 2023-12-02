import random
import numpy as np
import threading
import tkinter as tk
import copy
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Evolution logic classes
class Gene:
    def __init__(self, source_type, source_num, sink_type, sink_num, weight, source_pos=None, sink_pos=None):
        self.source_type = source_type
        self.source_num = source_num
        self.sink_type = sink_type
        self.sink_num = sink_num
        self.weight = weight
        self.source_pos = source_pos if source_pos else self.random_position()
        self.sink_pos = sink_pos if sink_pos else self.random_position()

    @staticmethod
    def random_position():
        return (random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1))

    def mutate(self):
        self.weight += random.uniform(-0.1, 0.1)

class Genome:
    def __init__(self, genes=None):
        self.genes = genes if genes else []

    def add_connection(self, source_type, source_num, sink_type, sink_num, weight, source_pos=None, sink_pos=None):
        gene = Gene(source_type, source_num, sink_type, sink_num, weight, source_pos, sink_pos)
        self.genes.append(gene)

    def deep_copy(self):
        return copy.deepcopy(self)

class Individual:
    def __init__(self, genome):
        self.genome = genome
        self.fitness = 0

    def evaluate_fitness(self):
        self.fitness = random.uniform(0, 10)

    def mutate(self):
        if not self.genome.genes:
            return
        gene_to_mutate = random.choice(self.genome.genes)
        gene_to_mutate.mutate()

class Evolution:
    def __init__(self, population_size, mutation_rate=0.1):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.population = [Individual(self.random_genome()) for _ in range(population_size)]
        self.generation = 0
        self.average_fitness = 0

    def random_genome(self):
        genes = [Gene('type1', 0, 'type2', 1, random.uniform(-1, 1)) for _ in range(random.randint(1, 3))]
        return Genome(genes)

    def run_generation(self):
        for individual in self.population:
            individual.evaluate_fitness()

        self.average_fitness = sum(ind.fitness for ind in self.population) / len(self.population)

        self.population.sort(key=lambda x: x.fitness, reverse=True)
        self.population = self.population[:self.population_size // 2]

        next_generation = self.create_next_generation()
        self.population = next_generation
        self.generation += 1

    def create_next_generation(self):
        next_generation = []
        while len(next_generation) < self.population_size:
            parent1, parent2 = random.sample(self.population, 2)
            child_genome = self.crossover(parent1.genome, parent2.genome)
            child = Individual(child_genome)
            if random.random() < self.mutation_rate:
                child.mutate()
            next_generation.append(child)
        return next_generation

    def crossover(self, genome1, genome2):
        new_genes = random.sample(genome1.genes, len(genome1.genes) // 2) + random.sample(genome2.genes, len(genome2.genes) // 2)
        if not new_genes:
            new_genes.append(random.choice(genome1.genes + genome2.genes))
        return Genome(new_genes)

# OpenGL-based visualization class
class OpenGLWidget:
    def __init__(self, evolution):
        self.evolution = evolution
        self.continue_running = True
        self.initialized = False

    def init_gl(self):
        pygame.init()
        pygame.display.set_mode((800, 800), DOUBLEBUF | OPENGL)
        gluPerspective(45, 1, 0.1, 50.0)
        glTranslatef(0, 0, -5)
        self.initialized = True
        
            def run_evolution(self):
        if not self.initialized:
            self.init_gl()

        while self.continue_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            self.evolution.run_generation()
            self.draw_gene_network()
            pygame.display.flip()
            time.sleep(0.5)

    def draw_gene_network(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glBegin(GL_LINES)
        if self.evolution.population:
            for gene in self.evolution.population[0].genome.genes:
                glColor3f(1, 0, 0)
                glVertex3fv(gene.source_pos)
                glVertex3fv(gene.sink_pos)
        glEnd()

    def stop(self):
        self.continue_running = False

# Tkinter-based GUI class
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

    def update_evolution_parameters(self):
        self.evolution.mutation_rate = self.mutation_scale.get()

    def start_evolution(self):
        self.update_evolution_parameters()
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.evolution_thread = threading.Thread(target=self.opengl_widget.run_evolution)
        self.evolution_thread.start()
        self.update_status()

    def stop_evolution(self):
        self.opengl_widget.stop()
        self.evolution_thread.join()
        self.stop_button.config(state=tk.DISABLED)
        self.start_button.config(state=tk.NORMAL)

    def update_status(self):
        if self.opengl_widget.continue_running:
            self.status_label.config(text=f"Generation: {self.evolution.generation}\nAverage Fitness: {self.evolution.average_fitness:.2f}")
            self.root.after(500, self.update_status)

    def run(self):
        self.root.mainloop()

def main():
    evolution = Evolution(population_size=100)
    opengl_widget = OpenGLWidget(evolution)
    gui = EvolutionGUI(evolution, opengl_widget)
    gui.run()

if __name__ == '__main__':
    main()
        