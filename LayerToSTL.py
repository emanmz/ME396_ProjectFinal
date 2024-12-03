# Import libraries
import cv2
import os
import numpy as np
from tkinter import *
from tkinter.filedialog import askopenfilename
from PIL import Image
import matplotlib.pyplot as plt
from stl import mesh

# --- STL Handling Functions ---
def save_to_stl(triangles, output_path):
    """
    Saves the generated triangles to an STL file.

    Args:
        triangles (list of tuple): List of 3D triangles.
        output_path (str): Path to save the STL file.
    """
    # Convert triangles into numpy array format
    stl_data = np.zeros(len(triangles), dtype=mesh.Mesh.dtype)
    for i, triangle in enumerate(triangles):
        stl_data['vectors'][i] = np.array(triangle)

    # Create and save the STL file
    extruded_mesh = mesh.Mesh(stl_data)
    extruded_mesh.save(output_path)

# --- Image Processing Functions ---
def generateContours(grayscale_folder, contour_folder):
    """
    Generates contour images from grayscale images with simplified and filled contours.

    Args:
        grayscale_folder (str): Path to the folder containing grayscale images.
        contour_folder (str): Path to save the contour images.
    """
    if not os.path.exists(contour_folder):
        os.makedirs(contour_folder)

    for image_name in os.listdir(grayscale_folder):
        image_path = os.path.join(grayscale_folder, image_name)
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            print(f"Failed to load image: {image_name}")
            continue

        # Apply thresholding to create a binary image
        ret, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
        
        # Find contours in the thresholded image
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if not contours:
            print(f"No contours found in file: {image_name}")
            continue

        # Simplify and fill each contour
        simplified_contours = []
        for contour in contours:
            # Approximate the contour to simplify it
            epsilon = 0.002 * cv2.arcLength(contour, True)
            simplified_contour = cv2.approxPolyDP(contour, epsilon, True)
            simplified_contours.append(simplified_contour)

        print(f"{len(simplified_contours)} simplified contours detected in {image_name}")

        # Create an empty black image with the same size as the input image
        contour_img = np.zeros_like(img)

        # Draw filled contours on the image (color 255 means white)
        cv2.drawContours(contour_img, simplified_contours, -1, (255), thickness=cv2.FILLED)

        output_path = os.path.join(contour_folder, f"contour_{image_name}")
        cv2.imwrite(output_path, contour_img)

# --- 3D Model Generation Functions ---
def create_base_layer(width, height, layer_thickness):
    """
    Create a base layer covering the dimensions of the image.

    Args:
        width (int): Width of the image.
        height (int): Height of the image.

    Returns:
        list of tuple: List of 3D triangles forming the base layer.
    """
    # Define the base corners at the bottom (z=0) and top (z=layer_thickness)
    base_bottom = [(0, 0, 0), (width, 0, 0), (width, height, 0), (0, height, 0)]
    base_top = [(0, 0, layer_thickness), (width, 0, layer_thickness), (width, height, layer_thickness), (0, height, layer_thickness)]

    # Create the bottom and top faces
    triangles = [
        (base_bottom[0], base_bottom[1], base_bottom[2]),
        (base_bottom[0], base_bottom[2], base_bottom[3]),
        (base_top[0], base_top[1], base_top[2]),
        (base_top[0], base_top[2], base_top[3]),
    ]

    # Create the sides connecting top and bottom faces
    for i in range(4):
        next_i = (i + 1) % 4
        triangles.append((base_bottom[i], base_bottom[next_i], base_top[i]))
        triangles.append((base_top[i], base_bottom[next_i], base_top[next_i]))

    return triangles

def extrude_contour_to_base(points, z_start, z_end):
    """
    Extrude a 2D contour to connect it to a base layer.

    Args:
        points (list of tuple): 2D contour points.
        z_start (float): Starting height of the layer.
        z_end (float): Ending height of the layer.

    Returns:
        list of tuple: List of 3D triangles forming the extruded layer.
    """
    triangles = []
    num_points = len(points)

    # Create top and bottom faces (caps)
    for i in range(1, num_points - 1):
        # Triangle fan for bottom cap
        triangles.append(((*points[0], z_start), (*points[i], z_start), (*points[i + 1], z_start)))
        # Triangle fan for top cap
        triangles.append(((*points[0], 0), (*points[i + 1], 0), (*points[i], 0)))

    # Create vertical walls
    for i in range(num_points):
        p1 = points[i]
        p2 = points[(i + 1) % num_points]

        # Define vertices for walls
        v1 = (*p1, z_start)
        v2 = (*p2, z_start)
        v3 = (*p1, 0)
        v4 = (*p2, 0)

        # Two triangles per wall segment
        triangles.append((v1, v2, v3))
        triangles.append((v3, v2, v4))

    return triangles

def createScad(grayscale_folder, contour_folder, stl_folder, height=5):
    """
    Generate a 3D model from grayscale images and save it as an STL file.
    Adds a base layer and ensures all layers connect to that base.

    Args:
        grayscale_folder (str): Path to the folder containing grayscale images.
        contour_folder (str): Path to the folder containing filled contour images.
        stl_folder (str): Path to save the final STL file.
        height (float): Height of each layer.
    """
    if not os.path.exists(contour_folder):
        raise FileNotFoundError(f"Contour folder does not exist: {contour_folder}")
    if not os.path.exists(stl_folder):
        os.makedirs(stl_folder)

    stl_triangles = []
    base_size = None

    for index, filename in enumerate(sorted(os.listdir(contour_folder))):
        file_path = os.path.join(contour_folder, filename)
        img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            print(f"Skipping invalid or unreadable image: {file_path}")
            continue

        # Find contours from the filled image
        contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            print(f"No contours found in file: {file_path}")
            continue

        if index == 0:
            h, w = img.shape
            base_size = (w, h)
            base_triangles = create_base_layer(w, h, 10)
            stl_triangles.extend(base_triangles)

        for contour in contours:
            points = [tuple(p[0]) for p in contour]
            if len(points) < 3:
                print(f"Skipping invalid contour with insufficient points: {len(points)}")
                continue

            z_start = (index * height) + 10
            z_end = (index + 1) * height + 10
            triangles = extrude_contour_to_base(points, z_start, z_end)
            stl_triangles.extend(triangles)

    if stl_triangles:
        stl_path = os.path.join(stl_folder, f"{os.path.basename(grayscale_folder)}.stl")
        save_to_stl(stl_triangles, stl_path)
        return stl_path
    else:
        print("No valid 3D model could be created from the provided contours.")
        return None