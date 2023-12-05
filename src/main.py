from evolution_gui import EvolutionVisPy

def main():
    evolution_pyvispy = EvolutionVisPy(population_size=100)
    for _ in range(100):  # Number of generations to visualize
        evolution_pyvispy.run_generation()

if __name__ == '__main__':
    main()
