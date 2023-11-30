import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QSlider, QLabel
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from mayavi import mlab
from tvtk.api import tvtk
from Evolve3D import Evolution  # Assuming Evolve3D.py contains the Evolution class

os.environ['QT_API'] = 'pyqt5'

class EvolutionThread(QThread):
    update_signal = pyqtSignal(int, float)

    def __init__(self, mayavi_widget, evolution):
        super().__init__()
        self.mayavi_widget = mayavi_widget
        self.evolution = evolution

    def run(self):
        self.mayavi_widget.run_evolution(self.update_signal)

class MayaviQWidget(QWidget):
    def __init__(self, parent=None):
        super(MayaviQWidget, self).__init__(parent)
        layout = QVBoxLayout(self)
        self.visualization_widget = self.create_mayavi_widget()
        layout.addWidget(self.visualization_widget)

    def create_mayavi_widget(self):
        from mayavi.core.ui.api import MayaviScene, MlabSceneModel, SceneEditor
        from traits.api import HasTraits, Instance
        from traitsui.api import View, Item

        class Container(HasTraits):
            scene = Instance(MlabSceneModel, ())

            @View
            def default_traits_view(self):
                return View(Item('scene', editor=SceneEditor(scene_class=MayaviScene),
                                 height=250, width=300, show_label=False))

        container = Container()
        mayavi_widget = QWidget()
        ui = container.edit_traits(parent=mayavi_widget, kind='subpanel').control
        return mayavi_widget

    def initialize(self, evolution):
        self.mayavi_widget = MayaviWidget(evolution, self.visualization_widget)

class MayaviWidget:
    def __init__(self, evolution, parent_widget):
        self.evolution = evolution
        self.figure = mlab.figure(size=(800, 800), bgcolor=(0.5, 0.5, 0.5))
        self.continue_running = True
        self.parent_widget = parent_widget

    def run_evolution(self, update_signal):
        while self.continue_running:
            self.evolution.run_generation()
            self.draw_gene_network()
            update_signal.emit(self.evolution.generation, self.evolution.average_fitness)
            QThread.msleep(500)

    def draw_gene_network(self):
        mlab.clf(self.figure)
        if self.evolution.population:
            for gene in self.evolution.population[0].genome.genes:
                pos = np.array([gene.source_pos, gene.sink_pos])
                mlab.plot3d(pos[:, 0], pos[:, 1], pos[:, 2], tube_radius=0.01, color=(1, 0, 0))

    def stop(self):
        self.continue_running = False

class EvolutionGUI(QMainWindow):
    def __init__(self, evolution):
        super().__init__()
        self.evolution = evolution
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Evolution Simulation')
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)

        self.layout = QVBoxLayout(self.main_widget)

        self.mayavi_qt_widget = MayaviQWidget(self)
        self.mayavi_qt_widget.initialize(self.evolution)
        self.layout.addWidget(self.mayavi_qt_widget)

        self.start_button = QPushButton('Start Evolution', self)
        self.start_button.clicked.connect(self.start_evolution)
        self.layout.addWidget(self.start_button)

        self.stop_button = QPushButton('Stop Evolution', self)
        self.stop_button.clicked.connect(self.stop_evolution)
        self.stop_button.setEnabled(False)
        self.layout.addWidget(self.stop_button)

        self.mutation_label = QLabel('Mutation Rate: 0.1', self)
        self.layout.addWidget(self.mutation_label)

        self.mutation_slider = QSlider(Qt.Horizontal, self)
        self.mutation_slider.setMinimum(0)
        self.mutation_slider.setMaximum(20)
        self.mutation_slider.setValue(int(self.evolution.mutation_rate * 100))
        self.mutation_slider.valueChanged[int].connect(self.change_mutation_rate)
        self.layout.addWidget(self.mutation_slider)

        self.status_label = QLabel('Generation: 0\nAverage Fitness: 0.0', self)
        self.layout.addWidget(self.status_label)

        self.evolution_thread = EvolutionThread(self.mayavi_qt_widget.mayavi_widget, self.evolution)
        self.evolution_thread.update_signal.connect(self.update_status)

    def start_evolution(self):
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.evolution_thread.start()

    def stop_evolution(self):
        self.mayavi_qt_widget.mayavi_widget.stop()
        self.evolution_thread.wait()
        self.stop_button.setEnabled(False)
        self.start_button.setEnabled(True)

    def change_mutation_rate(self, value):
        self.evolution.mutation_rate = value / 100.0
        self.mutation_label.setText(f'Mutation Rate: {self.evolution.mutation_rate:.2f}')

    def update_status(self, generation, avg_fitness):
        self.status_label.setText(f'Generation: {generation}\nAverage Fitness: {avg_fitness:.2f}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    evolution = Evolution(population_size=100)
    gui = EvolutionGUI(evolution)
    gui.show()
    sys.exit(app.exec_())
