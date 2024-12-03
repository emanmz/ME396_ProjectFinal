import cv2
import os
from tkinter import *
from tkinter.filedialog import askopenfilename
from OpenCVTest import greyScaleImage
from LayerToSTL import createScad, generateContours
import pyvista as pv

# Function to choose an image
def file_open():
    global file_path
    file_path = askopenfilename(
        initialdir='C:/', title='Select an Image File', filetypes=(("Image Files", "*.jpg *.png"), ("All Files", "*.*"))
    )
    if file_path:
        windows.destroy()  # Close the Tkinter window after selection
        return file_path
    else:
        print("No file selected. Exiting...")
        exit()
def simplify_stl(input_file, output_file, reduction_factor=0.5):
    """
    Simplify an STL file and save the result.
    
    Args:
        input_file (str): Path to the input STL file.
        output_file (str): Path to save the simplified STL file.
        reduction_factor (float): Fraction of the original number of triangles to retain (0 < reduction_factor <= 1).
    """
    # Load the STL file
    mesh = pv.read(input_file)

    # Simplify the mesh
    simplified_mesh = mesh.decimate(reduction_factor)

    # Save the simplified STL file
    simplified_mesh.save(output_file)
    print(f"Simplified STL saved to {output_file}")

if __name__ == '__main__':
    # Tkinter window for file selection
    windows = Tk()
    windows.title("Upload an Image!")
    windows.geometry("300x100")

    open_button = Button(windows, text="Open Image File (png or jpg only)", command=file_open)
    open_button.pack(pady=20)

    windows.mainloop()

    # Ensure file path validity
    if not file_path:
        print("No file selected. Exiting...")
        exit()

    # Set up base paths
    base_path = '/Users/emanz/Documents/ME396_ProjectFinal'
    file_name = os.path.basename(file_path)
    grayscale_folder = os.path.join(base_path, 'Grayscale')
    contour_folder = os.path.join(base_path, 'Contours')
    stl_folder = os.path.join(base_path, 'STL_Files')

    # Step 1: Convert image to grayscale and separate layers
    output_folder = greyScaleImage(file_path, grayscale_folder)
    print(f"Grayscale layers saved in: {output_folder}")
    
    # Step 2: Convert Greyscale to Contours
    generateContours(output_folder, contour_folder)
    
    stl_thing = createScad(output_folder, contour_folder, stl_folder, 2)
    simplify_stl(stl_thing, "simplified_model.stl", reduction_factor=0.3)
   # Load STL file
    mesh = pv.read(stl_thing)

    # Create a plotter object and display the STL
    plotter = pv.Plotter()
    plotter.add_mesh(mesh, color='lightblue')  # Add mesh with a color
    plotter.show()