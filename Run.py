import cv2
import os
import numpy as np
from tkinter import *
from tkinter.filedialog import askopenfilename
from PIL import Image
import matplotlib.pyplot as plt
from OpenCVTest import greyScaleImage
from LayerToSTL import process_image_to_contours, createScad

# Function to choose an image from the running computer's files! Returns the file path

def file_open():
    global file_path
    file_path = askopenfilename(
        initialdir='C:/', title='Select an Image File', filetypes=(("Image Files", "*.jpg *.png"), ("All Files", "*.*"))
    )
    if file_path:
        windows.destroy()  # Close the Tkinter window immediately after file selection
        return file_path
    else:
        print("No file selected. Exiting...")
        exit()
        
if __name__ == '__main__':
    # 1. Choose a file from computer running program
    # Tkinter window
    windows = Tk()
    windows.title("Upload an Image!")
    windows.geometry("300x100")

    # Add a button to open the file
    open_button = Button(windows, text="Open Image File (png or jpg only)", command=file_open)
    open_button.pack(pady=20)

    # Start Tkinter mainloop
    windows.mainloop()

    # Ensure the file path is valid
    if not file_path:
        print("No file selected. Exiting...")
        exit()

    # Setting up where to store images and STL files
    base_path = '/Users/emanzaheer/Documents/ME396_ProjectFinal'

    # 2. Convert image to grayscale and seperate them into layers. 
    # Images are labeled Image_1.png.. Image_2.png representing layers in the st.
    # 1 is the bottom, 2 is on top etc etc 
    grayscale_folder = greyScaleImage(file_path, base_path)
    print(f"Grayscale layers saved in: {grayscale_folder}")
    
    # 3. Process grayscale layers into contours
    contour_folder = os.path.join(base_path, 'Contours')
    process_image_to_contours(grayscale_folder, contour_folder)
    
    # 4. Generate 3D parts and combine into a single STL
    stl_folder = os.path.join(base_path, 'STL_Files')
    final_stl_path = createScad(contour_folder, stl_folder, height=5)
    print(f"Final STL saved at: {final_stl_path}")
