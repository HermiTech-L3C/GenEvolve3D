import wx
from Evolve3D import Evolution
from GUI import EvolutionGUI

def main():
    app = wx.App(False)
    evolution = Evolution(population_size=100)
    gui = EvolutionGUI(None, evolution)
    gui.Show(True)
    app.MainLoop()

if __name__ == '__main__':
    main()