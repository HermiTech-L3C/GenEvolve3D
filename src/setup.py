from cx_Freeze import setup, Executable
import sys

# Define the base for the executable
base = "Win32GUI" if sys.platform == "win32" else None

# List of required packages
required_packages = [
    "numpy",
    "PyQt5",  # Use "PyQt5" instead of "pyqt5"
    "vispy"
]

# Additional non-Python files that are needed
additional_files = [
    'evolution.py',
    'evolution_gui.py'
    # Add other necessary files here, like images, data files, etc.
]

# Build options for cx_Freeze
build_options = {
    "packages": required_packages,
    "include_files": additional_files
}

# Define the main script
main_script = "main.py"

# Setup script for building the executable
setup(
    name="GenEvolve3D",
    version="0.1",
    description="A 3D Genetic Algorithm Visualization Tool",
    options={"build_exe": build_options},
    executables=[Executable(main_script, base=base)]
)
