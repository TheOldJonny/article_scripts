import graph # Importing the functions implemented in graph.py
import sys
import os
import numpy as np



if len(sys.argv) != 10:
    print("Please, provide:")
    print("1) The path")
    print("2) The starting coordinates")
    print("3) The two atoms that define the distance")
    print("4) The 4 atoms that define the dihedral angle")
    print("5) The output filename")
    exit(-1)
    
try:
    path = sys.argv[1]
    filename = sys.argv[2]
    
    # 0 based indices of atoms
    
    # Indices for distance
    r1 = int(sys.argv[3])
    r2 = int(sys.argv[4])
    
    # Indices for dihedral angle
    rr1 = int(sys.argv[5])
    rr2 = int(sys.argv[6])
    rr3 = int(sys.argv[7])
    rr4 = int(sys.argv[8])
    
    outputFilename = sys.argv[9]
    
except TypeError:
    print("There is an error in parsing the provided information")
    exit(-1)
    
    

try:
    os.chdir(path)
except OSError:
    print("The inserted path is not consistent")
    exit(-1)
    
folders = os.listdir()



for folder in folders:
    os.chdir(folder)
    
    # print(os.listdir())
    
    
    

    t = graph.timeCatcher(filename)
    d = graph.distanceCatcher(filename, r1, r2)
    phi = graph.dihedralCatcher(filename, rr1, rr2, rr3, rr4)
    
    
    # saving the output
    graph.savingOutput(outputFilename= outputFilename, timeVector = t, distanceVector = d, dihedralVector = phi)
    
    # moving to the previous position
    os.chdir("..")

