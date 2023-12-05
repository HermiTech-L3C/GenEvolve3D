from vispy import app, scene
from evolution import Evolution, Position
import numpy as np

class EvolutionVisPy:
    def __init__(self, population_size):
        self.evolution = Evolution(population_size=population_size)
        self.canvas = scene.SceneCanvas(keys='interactive', show=True)
        self.view = self.canvas.central_widget.add_view()
        self.view.camera = 'turntable'  # or try 'arcball'
        scene.visuals.XYZAxis(parent=self.view.scene)

    def run_generation(self):
        self.evolution.run_generation()
        self.draw_gene_network()

    def draw_gene_network(self):
        for gene in self.evolution.population[0].genome.genes:
            self.draw_node(gene.source_pos)
            self.draw_node(gene.sink_pos)
            self.draw_connection(gene.source_pos, gene.sink_pos)

    def draw_node(self, position):
        sphere = scene.visuals.Sphere(radius=0.1, method='latitude', parent=self.view.scene,
                                      edge_color='black', color=(0.4, 0.4, 0.4, 1.0))
        sphere.transform = scene.transforms.STTransform(translate=(position.x, position.y, position.z))

    def draw_connection(self, source_pos, sink_pos):
        line = scene.visuals.Line(pos=np.array([[source_pos.x, source_pos.y, source_pos.z],
                                                [sink_pos.x, sink_pos.y, sink_pos.z]]),
                                  color='yellow', method='gl', parent=self.view.scene)
        line.transform = scene.transforms.STTransform()

if __name__ == '__main__':
    ev_vispy = EvolutionVisPy(population_size=100)
    for _ in range(100):  # Adjust the number of generations
        ev_vispy.run_generation()
    app.run()

