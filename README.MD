# Genetic Evolution Simulation
This project simulates genetic evolution through an artificial environment using neural networks and genetic algorithms. It visualizes the evolution process using 3D graphics.
## Description
This Python script models an evolutionary process where individuals in a population evolve over generations. Each individual has a genome that influences its survival in an environment. The program uses machine learning (MLPRegressor from scikit-learn) to simulate decision-making processes and Mayavi for 3D visualization of the genetic network.
## Getting Started
### Dependencies
Ensure you have the following installed:

Python 3.8 or above
NumPy
scikit-learn
Mayavi
PyQt5
Tkinter (usually comes pre-installed with Python)
### Installation

Clone this repository or download the script.
Install the required packages:
    ```
    pip install numpy scikit-learn mayavi PyQt5
    ```
### Running the Program
Run the script from your terminal:
```bash
python Evolve3D.py
```
## Features

**Genetic Algorithm**: Simulates natural selection and genetic mutation.
**Neural Network**: Each individual's decision-making is modeled using an MLPRegressor.
**3D Visualization**: Visualizes the genetic network using Mayavi.
**Interactive GUI**: Allows users to start, stop, and adjust parameters of the simulation in real-time.
## How to Use

Start the program.
Use the GUI to begin the simulation.
Adjust mutation rates using the slider.
Observe the evolution process in the 3D view.
Stop the simulation at any time.
## Contributing
Contributions to enhance or expand the functionality of this simulation are welcome. Please adhere to standard coding practices.
## Authors

['ANT 0, GREENE']
## License
This project is licensed under the MLP2.0 License - see the LICENSE.md file for details.
## Acknowledgments
Inspiration, code snippets, etc.
[Artificial Intelligence: A Modern Approach](http://aima.cs.berkeley.edu/)
[Scikit-learn Documentation](https://scikit-learn.org/stable/)
[Mayavi: 3D Scientific Data Visualization and Plotting](https://docs.enthought.com/mayavi/mayavi/)
