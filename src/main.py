import os
from evolution_gui import EvolutionPyThreejs
from evolution import Evolution

# Explicitly set the preferred toolkit before importing GUI modules
os.environ['ETS_TOOLKIT'] = 'qt'

def main():
    evolution = Evolution(population_size=100, fitness_function=lambda genome: sum(gene.activity for gene in genome.genes))
    evolution_pythreejs = EvolutionPyThreejs(population_size=100)

    for _ in range(100):  # Adjust the number of generations to visualize
        evolution.run_generation()
        evolution_pythreejs.run_generation()
        evolution_pythreejs.draw_gene_network()  # Visualize the best individual's gene network

    evolution_pythreejs.run()

if __name__ == '__main__':
    main()
