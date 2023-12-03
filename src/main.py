# main.py
import threading
import pygame
from GUI import EvolutionGUI, Evolution

def main():
    pygame.init()  # Initialize pygame

    evolution = Evolution(population_size=100)
    gui = EvolutionGUI(evolution)

    # Run the Tkinter main loop in a separate thread
    tkinter_thread = threading.Thread(target=gui.run, daemon=True)
    tkinter_thread.start()

    # Wait for Tkinter thread to finish
    tkinter_thread.join()

    pygame.quit()  # Properly close pygame

if __name__ == '__main__':
    main()
