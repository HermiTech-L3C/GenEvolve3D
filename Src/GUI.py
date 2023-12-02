import wx
import threading
import time
from mayavi import mlab
from Evolve3D import Evolution

class EvolutionThread(threading.Thread):
    def __init__(self, mayavi_widget, evolution, update_callback):
        threading.Thread.__init__(self)
        self.mayavi_widget = mayavi_widget
        self.evolution = evolution
        self.update_callback = update_callback
        self.daemon = True

    def run(self):
        while self.mayavi_widget.continue_running:
            self.evolution.run_generation()
            wx.CallAfter(self.update_callback, self.evolution.generation, self.evolution.average_fitness)
            time.sleep(0.5)

class MayaviWidget:
    def __init__(self, evolution, parent_widget):
        self.evolution = evolution
        self.figure = mlab.figure(size=(800, 800), bgcolor=(0.5, 0.5, 0.5))
        self.continue_running = True
        self.parent_widget = parent_widget

    def update_visualization(self):
        mlab.clf(self.figure)
        if self.evolution.population:
            for gene in self.evolution.population[0].genome.genes:
                pos = np.array([gene.source_pos, gene.sink_pos])
                mlab.plot3d(pos[:, 0], pos[:, 1], pos[:, 2], tube_radius=0.01, color=(1, 0, 0))

class EvolutionGUI(wx.Frame):
    def __init__(self, parent, evolution):
        wx.Frame.__init__(self, parent, title='Evolution Simulation', size=(800, 600))
        self.evolution = evolution
        self.initUI()

    def initUI(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        self.mayavi_widget = MayaviWidget(self.evolution, panel)
        # Integration of Mayavi widget in wxPython is handled here

        self.start_button = wx.Button(panel, label='Start Evolution')
        self.start_button.Bind(wx.EVT_BUTTON, self.start_evolution)
        vbox.Add(self.start_button, flag=wx.EXPAND|wx.ALL, border=5)

        self.stop_button = wx.Button(panel, label='Stop Evolution')
        self.stop_button.Bind(wx.EVT_BUTTON, self.stop_evolution)
        self.stop_button.Disable()
        vbox.Add(self.stop_button, flag=wx.EXPAND|wx.ALL, border=5)

        self.mutation_label = wx.StaticText(panel, label='Mutation Rate: 0.1')
        vbox.Add(self.mutation_label, flag=wx.ALL, border=5)

        self.mutation_slider = wx.Slider(panel, value=10, minValue=0, maxValue=20, style=wx.SL_HORIZONTAL)
        self.mutation_slider.Bind(wx.EVT_SLIDER, self.change_mutation_rate)
        vbox.Add(self.mutation_slider, flag=wx.EXPAND|wx.ALL, border=5)

        self.status_label = wx.StaticText(panel, label='Generation: 0\nAverage Fitness: 0.0')
        vbox.Add(self.status_label, flag=wx.ALL, border=5)

        panel.SetSizer(vbox)
        self.Show(True)

    def start_evolution(self, event):
        self.start_button.Disable()
        self.stop_button.Enable()
        self.evolution_thread = EvolutionThread(self.mayavi_widget, self.evolution, self.update_status)
        self.evolution_thread.start()

    def stop_evolution(self, event):
        self.mayavi_widget.continue_running = False
        self.evolution_thread.join()
        self.stop_button.Disable()
        self.start_button.Enable()

    def change_mutation_rate(self, event):
        value = self.mutation_slider.GetValue()
        self.evolution.mutation_rate = value / 100.0
        self.mutation_label.SetLabel(f'Mutation Rate: {self.evolution.mutation_rate:.2f}')

    def update_status(self, generation, avg_fitness):
        self.status_label.SetLabel(f'Generation: {generation}\nAverage Fitness: {avg_fitness:.2f}')

if __name__ == '__main__':
    app = wx.App(False)
    evolution = Evolution(population_size=100)
    gui = EvolutionGUI(None, evolution)
    app.MainLoop()
