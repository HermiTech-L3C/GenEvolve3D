# main.py

from evolution_gui import EvolutionGUI
from evolution import Evolution

def main():
    evolution = Evolution(population_size=100)
    gui = EvolutionGUI(evolution)
    gui.run()

if __name__ == '__main__':
    main()
