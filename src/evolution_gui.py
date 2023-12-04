# evolution_gui.py

import tkinter as tk
from mayavi import mlab
from traits.api import HasTraits, Instance
from traitsui.api import View, Item
from mayavi.core.ui.api import MlabSceneModel, SceneEditor
from evolution import Evolution

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
        # Adjust the number of generations to visualize
        if self.evolution.generation < 100:  
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
