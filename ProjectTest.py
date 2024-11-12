from tkinter import *
from tkinter.filedialog import askopenfilename
from PIL import Image
import matplotlib.pyplot as plt
import cv2

# Initialize the main Tkinter window
windows = Tk()
windows.title("Upload an Image!")
windows.geometry("250x50")

# Global variable to store the file path
file_path = None

def file_open():
    global file_path  # Access the global variable
    # Open file dialog to select an image file
    file_path = askopenfilename(
        initialdir='C:/', title='Select an Image File', filetypes=(("Image Files", "*.jpg *.png"), ("All Files", "*.*"))
    )
    
    if file_path:  # Check if a file was selected
        # Open the image using PIL
        img = Image.open(file_path)
        
        # Display the image using matplotlib
        plt.imshow(img)
        plt.axis('off')  # Turn off axes for better display
        plt.show()
        
        # Print the file path to verify it's stored
        print("File Path:", file_path)
        


# Button that opens the file dialog
open_button = Button(windows, text="Open Image File (png or jpg only)", command=file_open)
open_button.grid(row=4, column=3)

# Run the Tkinter event loop
windows.mainloop()
