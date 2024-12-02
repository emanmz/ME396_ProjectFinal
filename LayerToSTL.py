from OpenCVTest import greyScaleImage
import cv2
import os
import numpy as np


# Custom linear extrusion function
def linear_extrude(vertices, height, steps=1):
    """
    #Custom linear extrude function to create a 3D model from a 2D polygon.

    Args:
        vertices (list of tuple): List of (x, y) points defining the 2D polygon.
        height (float): Height to extrude the polygon.
        steps (int): Number of layers (vertical steps) for the extrusion.

    Returns:
        list of tuple: List of 3D triangles representing the extruded shape.
    """
    vertices = np.array(vertices)
    triangles = []  # To store the resulting 3D triangles

    # Generate layers at different heights
    for step in range(steps):
        z_start = (step / steps) * height
        z_end = ((step + 1) / steps) * height

        # Create the top and bottom faces
        if step == 0:  # Bottom face (first layer)
            triangles += triangulate_face(vertices, z_start)
        if step == steps - 1:  # Top face (last layer)
            triangles += triangulate_face(vertices, z_end)

        # Create side faces (connect corresponding vertices of adjacent layers)
        for i in range(len(vertices)):
            # Current and next vertices in the polygon
            v1 = (*vertices[i], z_start)
            v2 = (*vertices[(i + 1) % len(vertices)], z_start)
            v3 = (*vertices[i], z_end)
            v4 = (*vertices[(i + 1) % len(vertices)], z_end)

            # Form two triangles for the quad connecting these vertices
            triangles.append((v1, v2, v3))
            triangles.append((v3, v2, v4))

    return triangles


def triangulate_face(vertices, z):
    """
    Triangulates a 2D polygon to create a 3D face at height z.

    Args:
        vertices (list of tuple): List of (x, y) points defining the 2D polygon.
        z (float): Height at which to place the face.

    Returns:
        list of tuple: List of 3D triangles representing the face.
    """
    # Simple triangulation for convex polygons
    triangles = []
    for i in range(1, len(vertices) - 1):
        v0 = (*vertices[0], z)
        v1 = (*vertices[i], z)
        v2 = (*vertices[i + 1], z)
        triangles.append((v0, v1, v2))
    return triangles


# Function to process an image into contours
def process_image_to_contours(grayscale_folder, contour_folder, min_contour_area=50):
    if not os.path.exists(contour_folder):
        os.makedirs(contour_folder)

    # Loop through all grayscale layers in the folder
    for filename in sorted(os.listdir(grayscale_folder)):
        file_path = os.path.join(grayscale_folder, filename)
        img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)

        # Find contours
        contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Filter contours based on area and save them
        layer_contours = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > min_contour_area:
                layer_contours.append(contour)

        # Save contours for visualization
        contour_img = np.zeros_like(img)
        cv2.drawContours(contour_img, layer_contours, -1, (255), thickness=1)
        cv2.imwrite(os.path.join(contour_folder, f'Contours_{filename}'), contour_img)

    print(f"Contours saved in: {contour_folder}")
    return contour_folder


# Function to create 3D parts from contours and save as STL
def createScad(contour_folder, stl_folder, height=1):
    if not os.path.exists(stl_folder):
        os.makedirs(stl_folder)

    stl_triangles = []
    z_offset = 0  # Start Z-offset at 0

    # Process each layer in the contour folder
    for filename in sorted(os.listdir(contour_folder)):
        file_path = os.path.join(contour_folder, filename)
        img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)

        # Find contours
        contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Create 3D model for each layer
        for contour in contours:
            points = [tuple(p[0]) for p in contour]  # Convert to tuples
            triangles = linear_extrude(points, height=height, steps=10)
            # Adjust for Z-offset
            for triangle in triangles:
                stl_triangles.append([
                    (x, y, z + z_offset) for x, y, z in triangle
                ])

        # Increment Z offset for the next layer
        z_offset += height

    # Save as STL
    stl_path = os.path.join(stl_folder, "final_object.stl")
    save_to_stl(stl_triangles, stl_path)
    print(f"3D object saved as: {stl_path}")
    return stl_path


# Save triangles as STL
def save_to_stl(triangles, output_path):
    """
    Saves the generated triangles to an STL file.

    Args:
        triangles (list of tuple): List of 3D triangles.
        output_path (str): Path to save the STL file.
    """
    from stl import mesh

    # Convert triangles into numpy array format
    stl_data = np.zeros(len(triangles), dtype=mesh.Mesh.dtype)
    for i, triangle in enumerate(triangles):
        stl_data['vectors'][i] = np.array(triangle)

    # Create and save the STL file
    extruded_mesh = mesh.Mesh(stl_data)
    extruded_mesh.save(output_path)
    print(f"STL file saved at: {output_path}")
