import cv2
import os
import numpy as np
from tkinter import *
from tkinter.filedialog import askopenfilename
from PIL import Image
import matplotlib.pyplot as plt


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
     
def nothing(x): 
    pass

def greyScaleImage(file_path=None):
    # Load Image 
    image = cv2.imread(file_path)
    if image is None:
        print("Error loading image. Ensure it's a valid file.")
        exit()
    
    # Get the base name of the image (without extension)
    image_name = os.path.splitext(os.path.basename(file_path))[0]

    # Define the base path for the final project !!!
    # YOU DON'T NEED TO DO THIS! I did this because it was making a mess in my downloads 
    base_path = '/Users/emanzaheer/Documents/ME396_ProjectFinal'

    # Create a subfolder named after the image within the base path
    output_folder = os.path.join(base_path, image_name)

    # Ensure the subfolder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    print(f"Output folder created: {output_folder}")
    
    # Get the dimensions of the image
    height, width, _ = image.shape

    # Use the cvtColor() function to grayscale the image
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Set Trackbar Size
    trackbar = np.zeros((1,500,3), np.uint8)

    layer_num = 2

    while(1):
    
        # Start with an empty image for the customized image
        customized_image = np.zeros((height, width, 3), np.uint8)
    
        # Start with an empty image for the customized image
        combined_layers = np.zeros((height, width, 3), np.uint8)
    
        #Create Trackbar and ask for User Input
        WindowName = 'PRESS ENTER TO CONFIRM --- PRESS ESC TO EXIT'
        cv2.namedWindow(WindowName)
        cv2.createTrackbar('Layers', WindowName, layer_num, 255, nothing)
        cv2.setTrackbarMin('Layers', WindowName, 2)
        cv2.imshow(WindowName, trackbar)
    
    
        while(1):
            # Check if enter pressed
            k = cv2.waitKey()
            if k == 13:
                break
            elif k == 27:
                break
            else:
                continue
    
        # Main Loop stops if ESC key pressed 
        if k == 27:
            cv2.destroyAllWindows()
            break
    
        layer_num = cv2.getTrackbarPos('Layers', WindowName)
        cv2.destroyAllWindows()
        layer_div = round(255/layer_num)
        shade_div = 255/(layer_num-1)
    
        layer_white = np.zeros((height, width, 3), np.uint8)
        layer_white[:] = (255,255,255)
    
        # Create each layer
        for i in range(0,layer_num):
            layer_shade = np.zeros((height, width, 3), np.uint8)
            layer_shade[:] = (shade_div*(layer_num-1-i), shade_div*(layer_num-1-i), shade_div*(layer_num-1-i))
        
            if i == 0:
                # Use inRange() to grab only one portion of the image
                image_portion = cv2.inRange(gray_image, layer_div*(layer_num-(i+1)), 255)
            elif i == layer_num-1:
                # Use inRange() to grab only one portion of the image
                image_portion = cv2.inRange(gray_image, 0, layer_div*(layer_num-i))
            else:
                # Use inRange() to grab only one portion of the image
                image_portion = cv2.inRange(gray_image, layer_div*(layer_num-(i+1)), layer_div*(layer_num-i)-1)
    
            # Color each portion
            portion_colored = cv2.bitwise_or(layer_shade, layer_shade, mask=image_portion)
            portion_white = cv2.bitwise_or(layer_white, layer_white, mask=image_portion)
    
            # Combine Colored Portions
            customized_image = cv2.bitwise_or(customized_image, portion_colored)
            combined_layers = cv2.bitwise_or(combined_layers, portion_white)
        
            # Save each layer into the created folder
            layer_path = os.path.join(output_folder, f'Layer_{layer_num - i}.png')
            cv2.imwrite(layer_path, portion_white)
            cv2.imshow(f'Layer_{layer_num - i}', portion_white)
    
        cv2.imshow('Original Grayscale', gray_image)
        cv2.imshow('Combined Image', customized_image)
    
        instructions = np.zeros((1,600,3), np.uint8)
        instructions[:] = (0, 0, 0)
        cv2.imshow('PRESS ENTER TO SAVE AND CONTINUE --- PRESS ESC TO SAVE AND QUIT', instructions)
    
        while(1):
            # Check if enter pressed
            k = cv2.waitKey()
            if k == 13:
                cv2.destroyAllWindows()
                break
            elif k == 27:
                break
            else:
                continue
    
        # Main Loop stops if ESC key pressed 
        if k == 27:
            cv2.destroyAllWindows()
            break
    
if __name__ == '__main__':
    # Initialize the main Tkinter window
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

    greyScaleImage(file_path)