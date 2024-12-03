# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 11:27:45 2024

@author: emanz
"""
import subprocess
import sys

# List of required libraries
required_libraries = [
    "cv2",           # OpenCV
    "numpy",         # NumPy
    "PIL",           # Pillow for image handling
    "matplotlib",    # Matplotlib for plotting
    "tkinter",       # Tkinter for GUI (built-in with Python)
    "stl",           # numpy-stl for STL handling
    "pyvista",       # PyVista for 3D visualization
]

# Function to install a library
def install_library(library_name, pip_name=None):
    pip_name = pip_name or library_name
    try:
        print(f"Checking {library_name}...")
        __import__(library_name)
    except ImportError:
        print(f"{library_name} is not installed. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", pip_name])

# all required libraries
for lib in required_libraries:
    # libraries whose import names differ from their pip package names
    pip_package_name = {
        "cv2": "opencv-python",   # OpenCV's pip package
        "stl": "numpy-stl",       # numpy-stl's pip package
        "Pillow": "PIL",       # Pillow (pip name matches)
        "pyvista": "pyvista"      # PyVista
    }.get(lib, lib)
    
    install_library(lib, pip_package_name)

print("All necessary libraries are installed.")

