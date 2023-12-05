from cx_Freeze import setup, Executable

# Specify the list of required packages
packages = ["numpy", "pyface", "traits", "mayavi", "vtk", "pythreejs"]

# Additional non-Python files that might be needed (modify as required)
include_files = ['evolution.py', 'evolution_gui.py']  # Include other necessary files

# Build options for cx_Freeze
build_exe_options = {
    "packages": packages,
    "include_files": include_files
}

# Specify the path to your main.py relative to the script location
# In this case, it assumes main.py is in the same directory as setup.py
main_script = "main.py"

# Setup script for building the executable
setup(
    name="GenEvolve3D",
    version="0.1",
    description="GenEvolve3D Application",
    options={"build_exe": build_exe_options},
    executables=[Executable(main_script, base=None)]
)
