# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 22:26:44 2024

@author: Alyssa Burtscher
"""

import openpyscad as ops

def createScad(points, layerHeight):
    scad = None
    height = 0.0
    
    for array in points:
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
        
        if scad is None:
            scad = ops.Polyhedron(points=p, faces=f)
        else:
            scad += ops.Polyhedron(points=p, faces=f)
        
    scad.write("ScadTest.scad")
    
if __name__ == '__main__':
    points = [[[-10, 0], [-5, 5], [5, 5], [10, 0], [5, -5], [-5, -5]], [[-5, 0], [-2.5, 2.5], [2.5, 2.5], [5, 0], [2.5, -2.5], [-2.5, -2.5]]]
    layerHeight = 10.0
    createScad(points, layerHeight)