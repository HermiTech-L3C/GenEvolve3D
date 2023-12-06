from vispy import app, gloo
from evolution import Evolution, Position
import numpy as np

vertex_shader = """
#version 330
uniform mat4 model;
in vec3 a_position;
out vec4 v_color;
void main() {
    gl_Position = model * vec4(a_position, 1.0);
    v_color = vec4(0.4, 0.4, 0.4, 1.0);
}
"""

fragment_shader = """
#version 330
in vec4 v_color;
out vec4 fragColor;
void main() {
    fragColor = v_color;
}
"""

class EvolutionVisPy:
    def __init__(self, population_size, vertex_shader, fragment_shader):
        self.evolution = Evolution(population_size=population_size)
        self.canvas = app.Canvas(keys='interactive', show=True)
        self.model = np.eye(4, dtype=np.float32)

        # Initialize with initial data
        self.nodes_data = gloo.VertexBuffer(self.get_node_positions())
        self.connections_data = gloo.VertexBuffer(self.get_connection_positions())

        self.program = gloo.Program(vertex_shader, fragment_shader)
        self.program['model'] = self.model
        self.program['a_position'] = self.nodes_data
        self.program['connections'] = self.connections_data

        self.canvas.measure_fps()
        self.timer = app.Timer(connect=self.update, start=True, interval=0.1)

    def get_node_positions(self):
        return np.array([gene.source_pos.xyz for gene in self.evolution.population[0].genome.genes], dtype=np.float32)

    def get_connection_positions(self):
        source_positions = np.array([gene.source_pos.xyz for gene in self.evolution.population[0].genome.genes], dtype=np.float32)
        sink_positions = np.array([gene.sink_pos.xyz for gene in self.evolution.population[0].genome.genes], dtype=np.float32)
        return np.column_stack((source_positions, sink_positions))

    def setup_nodes(self):
        self.nodes_data.set_data(self.get_node_positions())

    def setup_connections(self):
        self.connections_data.set_data(self.get_connection_positions())

    def run_generation(self):
        self.evolution.run_generation()

    def update_visuals(self):
        self.setup_nodes()
        self.setup_connections()
        self.canvas.update()

    def update(self, event):
        self.run_generation()
        self.update_visuals()

    def on_draw(self, event):
        gloo.set_state(blend=True, depth_test=True)
        gloo.clear(color='black', depth=True)

        self.program.draw('points')
        self.program.draw('lines')

if __name__ == '__main__':
    ev_vispy = EvolutionVisPy(population_size=100, vertex_shader=vertex_shader, fragment_shader=fragment_shader)
    ev_vispy.canvas.events.draw.connect(ev_vispy.on_draw)
    app.run()