import cv2
import os
import numpy as np
from tkinter import *
from tkinter.filedialog import askopenfilename
from PIL import Image
import matplotlib.pyplot as plt
from OpenCVTest import greyScaleImage
 
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

    # Setting up where I want all my images to go
    base_path = '/Users/emanzaheer/Documents/ME396_ProjectFinal'
    
    # 2. Grey scale the images and seperate each greyscale into a black and white png
    # These pngs are uploaded into a folder that is named after the original image
    # The folder is within whatever base path you have chosen
    greyScaleImage(file_path, base_path)