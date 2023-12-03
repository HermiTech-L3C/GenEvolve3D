# main.py
import threading
from GUI import EvolutionGUI, Evolution

def main():
    evolution = Evolution(population_size=100)
    gui = EvolutionGUI(evolution)

    # Run the Tkinter main loop in a separate thread
    tkinter_thread = threading.Thread(target=gui.run)
    tkinter_thread.start()

    # Main thread handles pygame events
    gui.handle_pygame_events()

    # Wait for Tkinter thread to finish
    tkinter_thread.join()

if __name__ == '__main__':
    main()
