# -*- coding: utf-8 -*-
# @author: Alyssa Burtscher

import numpy as np
from stl import mesh
import os

def createScad(points, layerHeight, name):
    if name[-4:] == ".stl" or name[-4:] == ".STL":
        name = name[:-4]
        
    d = name + " Individual Layers"
    if  not os.path.isdir(d):
        os.mkdir(d)
        
    stl_files = []
    height = 0.0
    layerNum = 0
    
    for array in points:
        layerNum += 1
        # Points Array (p) & Face Array (f)
        p = []
        f = []
        
        # Bottom Points
        for a in array:
            p.append([a[0], a[1], height])
            
        # Top Points
        height += layerHeight
        for a in array:
            p.append([a[0], a[1], height])
        
        count = len(array)
        
        # Bottom Face
        append1 = []
        for i in range(0, count):
            append1.append(i)
        f.append(append1)
        
        # Side Faces
        for k in range(count-1):
            l = k + count
            append2 = [k, k+1, l+1, l]
            f.append(append2)
        f.append([(count-1), 0, count, ((2*count)-1)])
        
        # Top Face
        append3 = []
        for j in range(count, count*2):
            append3.append(j)
        f.append(append3)
        
        # Chat GPT
        vertices = np.array(p)  # Ensure points are in a numpy array
        all_faces = []
        
        # Triangulate each face
        for face in f:
            if len(face) > 3:  # If the face has more than 3 vertices, triangulate it
                triangles = triangulate_face([vertices[i] for i in face])
                all_faces.extend(triangles)
            else:
                all_faces.append([vertices[i] for i in face])  # No triangulation needed for triangle faces
        
        # Convert the faces list into a numpy array
        all_faces = np.array(all_faces)
        
        # Create a mesh object
        your_mesh = mesh.Mesh(np.zeros(all_faces.shape[0], dtype=mesh.Mesh.dtype))
        
        # Set vertices for each face in the mesh
        for i, face in enumerate(all_faces):
            for j in range(3):  # Each face has 3 vertices
                your_mesh.vectors[i][j] = face[j]
        
        s = d + "\\" + name + "_Layer_{}.stl".format(layerNum)
        stl_files.append(s)
        
        # Write the mesh to an STL file
        your_mesh.save(s)
        
    output_filename = name + '.stl'

    merge_multiple_stl_files(stl_files, output_filename)
 
# Chat GPT
def triangulate_face(polygon):
    """
    Triangulate a polygon with more than 3 vertices by splitting it into triangles.
    A simple triangulation method is used here.
    For a polygon with n vertices, the first triangle is always formed by the first three vertices.
    Then we form new triangles by connecting the first vertex with the rest of the polygon's vertices.
    
    :param polygon: List of vertices of the polygon.
    :return: List of triangles, each triangle being a list of 3 vertices.
    """
    triangles = []
    num_vertices = len(polygon)
    
    # Triangulate the polygon by creating triangles from vertex 0
    for i in range(1, num_vertices - 1):
        triangles.append([polygon[0], polygon[i], polygon[i + 1]])
    
    return triangles

# Chat GPT
def merge_multiple_stl_files(stl_files, output_filename):
    # Load the first STL file
    first_mesh = mesh.Mesh.from_file(stl_files[0])
    combined_vertices = first_mesh.vectors
    
    # Iterate through the rest of the STL files and merge them
    for stl_file in stl_files[1:]:
        current_mesh = mesh.Mesh.from_file(stl_file)
        combined_vertices = np.concatenate([combined_vertices, current_mesh.vectors], axis=0)
    
    # Create a new mesh for the combined data
    merged_mesh = mesh.Mesh(np.zeros(combined_vertices.shape[0], dtype=mesh.Mesh.dtype))
    merged_mesh.vectors = combined_vertices
    
    # Save the merged mesh to an output STL file
    merged_mesh.save(output_filename)
    

if __name__ == '__main__':
    points = [[[-10, 0], [-5, 5], [5, 5], [10, 0], [5, -5], [-5, -5]], [[-5, 0], [-2.5, 2.5], [2.5, 2.5], [5, 0], [2.5, -2.5], [-2.5, -2.5]]]
    layerHeight = 10.0
    createScad(points, layerHeight, "HexagonsTest.stl")