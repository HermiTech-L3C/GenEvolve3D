from cx_Freeze import setup, Executable
import sys
import os

def get_base():
    return "Win32GUI" if sys.platform == "win32" else None

def get_required_packages():
    return [
        "numpy",
        "PyQt5",  # Use "PyQt5" instead of "pyqt5"
        "vispy"
    ]

def get_additional_files():
    return [
        'src/evolution.py',
        'src/evolution_gui.py'
        # Add other necessary files here, like images, data files, etc.
    ]

def build_options():
    return {
        "packages": get_required_packages(),
        "include_files": get_additional_files()
    }

def create_setup():
    base = get_base()
    main_script = "src/main.py"

    return setup(
        name="GenEvolve3D",
        version="0.1",
        description="A 3D Genetic Algorithm Visualization Tool",
        options={"build_exe": build_options()},
        executables=[Executable(main_script, base=base)]
    )

if __name__ == "__main__":
    create_setup()
