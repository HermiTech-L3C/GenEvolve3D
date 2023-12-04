# main.py

import os

# Explicitly set the preferred toolkit before importing GUI modules
# Change to 'qt' if using PyQt5
os.environ['ETS_TOOLKIT'] = 'qt'

from evolution_gui import EvolutionGUI
from evolution import Evolution

def main():
    evolution = Evolution(population_size=100)
    gui = EvolutionGUI(evolution)
    gui.run()

if __name__ == '__main__':
    main()
