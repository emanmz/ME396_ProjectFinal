import cv2
import os
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.simpledialog import askfloat, askstring
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
    return output_file

def delete_files_in_directory(directory_path):
   try:
     files = os.listdir(directory_path)
     for file in files:
       file_path = os.path.join(directory_path, file)
       if os.path.isfile(file_path):
         os.remove(file_path)
     print("All files deleted successfully.")
   except OSError:
     print("Error occurred while deleting files.")

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
    """
    CHANGE THE BELOW BASE PATH FOR WHEREVER YOU HAVE THIS REPOSITORY
    """
    base_path = '/Users/emanz/Documents/ME396_ProjectFinal'
    
    file_name = os.path.basename(file_path)
    grayscale_folder = os.path.join(base_path, 'Grayscale')
    contour_folder = os.path.join(base_path, 'Contours')
    delete_files_in_directory(contour_folder)
    stl_folder = os.path.join(base_path, 'STL_Files')

    # Step 1: Convert image to grayscale and separate layers
    output_folder = greyScaleImage(file_path, grayscale_folder)
    print(f"Grayscale layers saved in: {output_folder}")
    
    # Step 2: Convert Greyscale to Contours
    generateContours(output_folder, contour_folder)
    # Step 3: STL! 
    layer_thickness = askfloat("Input", "Enter layer thickness (e.g., 20):", minvalue=0.1)
    base_thickness = askfloat("Input", "Enter base thickness (e.g., 100):", minvalue=0.1)
    stl_thing = createScad(output_folder, contour_folder, stl_folder, layer_thickness, base_thickness)
    print(f"STL is saved in: {stl_thing}")
    mesh = pv.read(stl_thing)
    # Create a plotter object and display the STL
    plotter = pv.Plotter()
    plotter.add_mesh(mesh, color='lightblue')  # Add mesh with a color
    plotter.show()
    # Step 4: simplify the stl or not?
    simplify_or_no = askstring("Input", "Do you want to simplify the STL (recommended) (Y or N):")
    # Step 5: View the STL
    if simplify_or_no == "Y":
        simplify_stl(stl_thing, f"{file_name}_simplified.stl", reduction_factor=0.25)
        # # Load STL file
        mesh = pv.read(stl_thing)
        # Create a plotter object and display the STL
        plotter = pv.Plotter()
        plotter.add_mesh(mesh, color='lightblue')  # Add mesh with a color
        plotter.show()
    elif simplify_or_no == "N":
        mesh = pv.read(stl_thing)
        # Create a plotter object and display the STL
        plotter = pv.Plotter()
        plotter.add_mesh(mesh, color='green')  # Add mesh with a color
        plotter.show()
    else:
        print("You did not type in a Y or N.")
    
    
    