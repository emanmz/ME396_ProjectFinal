# README

## Tactile Image Generation: 2D Image -> 3D STL

### Overview

This Python project is a comprehensive tool for converting images into STL (3D model) files by converting images into grayscale layers, generating contours, and then into 3D models. It supports simplifying and visualizing 3D models, making it suitable for prototyping, 3D printing, and design visualization.

### Features
- Converts images to grayscale and separates them into multiple layers.
- Generates simplified and filled contours from grayscale images.
- Creates STL files from contours and supports mesh simplification.
- Visualizes STL files using PyVista.

### Prerequisites
- Python 3.8 or later
- Required libraries: OpenCV, NumPy, Pillow (PIL), Matplotlib, numpy-stl, PyVista, and Tkinter (built-in with Python).

### Installation
The **CheckYourLibraries.py** automatically installs missing dependencies. If required, install them manually using the following command:
```bash
pip install opencv-python numpy Pillow matplotlib numpy-stl pyvista
```

### How to Use

1. **Image Selection**:
   - Run the script **Run.py**.
   - A GUI window will prompt you to select an image file (`.png` or `.jpg`).

2. **Image Processing**:
   - Convert the selected image to grayscale layers by choosing the number of layers via a slider.
   - Save grayscale layers in a specified folder.

3. **Generate Contours**:
   - The contours are created from the grayscale images and saved in a separate folder.

4. **STL File Creation**:
   - Generate STL files from contours with user-defined extrusion parameters.
   - Simplify STL files to reduce the number of triangles for optimized 3D printing or visualization.

5. **STL Visualization**:
   - Visualize the generated STL files in 3D using PyVista.

### File Structure
- **Input**: Image files (`.png` or `.jpg`)
- **Output**:
  - Grayscale layers: `/Grayscale`
  - Contours: `/Contours`
  - STL files: `/STL_Files`

### Key Functions
1. **Image to Grayscale Layers**: `greyScaleImage()`
   - Converts an image to a grayscale image into black and white layers.

2. **Contour Generation**: `generateContours()`
   - Extracts and simplifies contours from black and white layers.

3. **STL File Creation**: `createScad()`
   - Converts contours into 3D models and saves them as STL files.

4. **STL Simplification (Optional but Recommended)**: `simplify_stl()`
   - Reduces the complexity of STL files by decimating the mesh.

### Basic Explanation

1. **Image Selection**:
   ```python
   file_open()
   ```

2. **Grayscale Conversion**:
   ```python
   greyScaleImage(file_path, grayscale_folder)
   ```

3. **Generate Contours**:
   ```python
   generateContours(grayscale_folder, contour_folder)
   ```

4. **Create and Simplify STL**:
   ```python
   createScad(output_folder, contour_folder, stl_folder, 20)
   simplify_stl("model.stl", "simplified_model.stl", reduction_factor=0.3)
   ```

5. **Visualize STL**:
   ```python
   mesh = pv.read("simplified_model.stl")
   plotter = pv.Plotter()
   plotter.add_mesh(mesh, color='lightblue')
   plotter.show()
   ```

### Notes
- Ensure valid file paths for input images and output folders.
- Close the GUI window before proceeding with further processing steps.
- For large images or complex contours, processing may take longer.

### Dependencies
- **OpenCV**: Image processing
- **NumPy**: Numerical computations
- **Pillow**: Image handling
- **Matplotlib**: Visualization (optional)
- **numpy-stl**: STL file creation
- **PyVista**: 3D visualization

### Contact
For questions or contributions, contact [Eman Zaheer](mailto:emanzaheer@utexas.edu), [Conner Petru](mailto:connerpetru@utexas.edu), or [Alyssa Burtscher](mailto:alyssa.burtscher@utexas.edu).
