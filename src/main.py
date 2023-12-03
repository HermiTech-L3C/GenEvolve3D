import threading
from GUI import EvolutionGUI, Evolution

def main():
    evolution = Evolution(population_size=100)
    gui = EvolutionGUI(evolution)
    gui.run()

if __name__ == '__main__':
    main()
