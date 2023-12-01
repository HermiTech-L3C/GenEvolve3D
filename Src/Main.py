from Evolve3D import Evolution
from GUI import EvolutionGUI
from PyQt5.QtWidgets import QApplication
import sys

def main():
    app = QApplication(sys.argv)
    evolution = Evolution(population_size=100)
    gui = EvolutionGUI(evolution)
    gui.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
