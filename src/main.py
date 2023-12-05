import os

# Explicitly set the preferred toolkit before importing GUI modules
# Change to 'qt' if using PyQt5
os.environ['ETS_TOOLKIT'] = 'qt'

from evolution_pythreejs import EvolutionPyThreejs
from evolution import Evolution

def main():
    evolution = Evolution(population_size=100)
    evolution_pythreejs = EvolutionPyThreejs(population_size=100)

    while evolution_pythreejs.generation < 100:  # Adjust the number of generations to visualize
        evolution.run_generation()
        evolution_pythreejs.update_status()

    evolution_pythreejs.run()

if __name__ == '__main__':
    main()
