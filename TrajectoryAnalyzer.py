import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import math
import sys

# Function that contatenates an arbitrary number of numpy arrays and it saves them in a file
def savingOutput(outputFilename: str, **kwargs: np.ndarray) -> None:
    
    header = ''
    matrix = []
    for key, value in kwargs.items():
        header = header + " " + key
        matrix.append(value)  
    
    
    np.savetxt(outputFilename, matrix, header = header, comments = '', delimiter = ' ')
        
    
# It returns the number of atoms from a coordinate file in XYZ format
def nAtomsFromXYZ(inputName: str)->int:
    try:
        f = open(inputName, 'r')
        n = int(f.readline().strip())
    except:
        print("There is an error in parsing the file")
        exit(-1)
    
    f.close()
    return n

# It returns the distance between two points given as numpy arrays
def distance(r1: np.ndarray, r2: np.ndarray) -> float:
    d = 0.
    for i in range(0, 3):
        d += (r1[i] - r2[i]) ** 2.
    
    d = math.sqrt(d)
    return d



# Function that calculates the bond angle given the positions of 3 atoms as numpy arrays
def angle(r1: np.ndarray, r2: np.ndarray, r3: np.ndarray) -> float:
    theta = 0.
    
    # The two vectors
    r21 = r1 - r2
    r32 = r3 - r2
    
    # Normalization 
    r21 = r21/np.linalg.norm(r21)
    r32 = r32/np.linalg.norm(r32)
    
    theta = math.acos(np.inner(r21, r32))
    
    theta = math.degrees(theta)
    return theta

# Function that calculates the dihedral angle given the positions of 4 atoms as numpy arrays
def dihedral(r1: np.ndarray, r2: np.ndarray, r3: np.ndarray, r4: np.ndarray) -> float:
    
    # The 3 vectors
    r21 = r1 - r2
    r32 = r3 - r2
    r43 = r4 - r3
    
    # The normal vectors to the planes
    n1 = np.cross(r21, r32)
    n2 = np.cross(r43, r32)
    
    # Normalization
    n1 = n1/np.linalg.norm(n1)
    n2 = n2/np.linalg.norm(n2)
    
    # calculating the angle between the normal vectors
    theta = math.acos(np.inner(n1, n2))
    
    
    # dihedral angle in degrees
    theta = math.degrees(theta)
    
    return theta
    
# It stores the time in a xyz trajectory file in a numpy array
def timeCatcher(filename: str) -> np.ndarray:
    with open(filename, 'r') as positions:
        timeAxis = []
        for line in positions:
            if ('time' in line):
                # It selects the time value in femntoseconds
                line = line.split()[5].strip(',')
                timeAxis.append(line)
                
    timeAxis = np.array(timeAxis, dtype= 'float')
    return timeAxis

# It stores the bond distance between two atoms in a xyz trajectory in a numpy array
def distanceCatcher(filename: str, firstAtom: int, secondAtom: int) -> np.ndarray:
    d = []
    
    nAtoms = nAtomsFromXYZ(filename)
    nHeader = 2
    
    # 0 based indices
    firstAtom -= 1
    secondAtom -= 1
    
    mylist = [firstAtom, secondAtom]
    sortedList = sorted(mylist)
    
    with open (filename, 'r') as f:
        condition = True
        while condition:
            for i in range(0, sortedList[0] + nHeader):
                try:
                    next(f)
                except:
                    condition = False
                    break
              
            atom1 = f.readline().split()
               
            # print(f.readline())     
        
            for i in range(0, sortedList[1] - sortedList[0] - 1):
                try:
                    next(f)
                except:
                    condition = False
                    break
            
            atom2 = f.readline().split()
            
            # print(f.readline())
            
            if (len(atom1) == 0 or len(atom2) == 0):
                break
            
            # storing the selected coordinates as numpy arrays
            del atom1[0]
            atom1 = np.array(atom1, dtype='float')
            del atom2[0]
            atom2 = np.array(atom2, dtype='float')
            
            d.append(distance(atom1, atom2))
        
            for i in range(0, nAtoms - sortedList[1] - 1):
                try:
                    next(f)
                except:
                    condition = False
                    break
                    
    d = np.array(d, dtype='float')
    return d

# It stores the bond angle between three atoms in a xyz trajectory in a numpy array
def angleCatcher(filename: str, firstAtom: int, secondAtom: int, thirdAtom: int) -> np.ndarray:
    d = []
    nHeader = 2
    
    nAtoms = nAtomsFromXYZ(filename)
    # 0 based indices
    firstAtom -= 1
    secondAtom -= 1
    thirdAtom -= 1
    

    # I need to sort the list to take the selected positions in order.
    # Anyway, I need to used the order of the initial list to calculate
    # the angle properly
    
    # I will use a dictionary to preserve the order
    
    mydict = {"a1" : firstAtom, "a2" : secondAtom, "a3" : thirdAtom}
    
    sorted_keys = sorted(mydict, key=mydict.get)
    
    
    sorted_dict = {}
    # Now I am sorting the dictionay by value
    for w in sorted_keys:
        sorted_dict[w] = mydict[w]
        
    sortedList = list(sorted_dict.values())
    
    
    with open (filename, 'r') as f:
        positionDict = {}
        
        condition = True
        while condition:
            for i in range(0, sortedList[0] + nHeader):
                try:
                    next(f)
                except:
                    condition = False
                    break
              
            atom1 = f.readline().split()
            # print(f.readline())     
        
            for i in range(0, sortedList[1] - sortedList[0] - 1):
                try:
                    next(f)
                except:
                    condition = False
                    break
            
            atom2 = f.readline().split()
            
            for i in range(0, sortedList[2] - sortedList[1] - 1):
                try:
                    next(f)
                except:
                    condition = False
                    break
            
            atom3 = f.readline().split()
            
            if (len(atom1) == 0 or len(atom2) == 0 or len(atom3) == 0):
                break
            
            # storing the selected coordinates as numpy arrays
            del atom1[0]
            atom1 = np.array(atom1, dtype='float')
            del atom2[0]
            atom2 = np.array(atom2, dtype='float')
            del atom3[0]
            atom3 = np.array(atom3, dtype='float')
            
            positionDict[sorted_keys[0]] = atom1  
            positionDict[sorted_keys[1]] = atom2   
            positionDict[sorted_keys[2]] = atom3    
             
            
            # Here I calculate the bond angle according to the initial order. How to do it?
            d.append(angle(positionDict["a1"], positionDict["a2"], positionDict["a3"]))
        
            for i in range(0, nAtoms - sortedList[2] - 1):
                try:
                    next(f)
                except:
                    condition = False
                    break
                    
    d = np.array(d, dtype='float')
    return d

# It stores the dihedral angle between four atoms in a xyz trajectory in a numpy array
def dihedralCatcher(filename: str, firstAtom: int, secondAtom: int, thirdAtom: int, fourthAtom: int) -> np.ndarray:
    # Empty list that will contain the dihedrals to be printed on file
    d = []
    nHeader = 2
    
    nAtoms = nAtomsFromXYZ(filename)
    
    # 0 based indices
    firstAtom -= 1
    secondAtom -= 1
    thirdAtom -= 1
    fourthAtom -= 1
    

    # I need to sort the list to take the selected positions in order.
    # Anyway, I need to used the order of the initial list to calculate
    # the dihedral properly
    
    # I will use a dictionary to preserve the order
    
    mydict = {"a1" : firstAtom, "a2" : secondAtom, "a3" : thirdAtom, "a4" : fourthAtom}
    
    sorted_keys = sorted(mydict, key=mydict.get)
    
    
    sorted_dict = {}
    # Now I am sorting the dictionay by value
    for w in sorted_keys:
        sorted_dict[w] = mydict[w]
        
    sortedList = list(sorted_dict.values())
    
    
    with open (filename, 'r') as f:
        positionDict = {}
        
        condition = True
        while condition:
            for i in range(0, sortedList[0] + nHeader):
                try:
                    next(f)
                except:
                    condition = False
                    break
              
            atom1 = f.readline().split()
            # print(f.readline())     
        
            for i in range(0, sortedList[1] - sortedList[0] - 1):
                try:
                    next(f)
                except:
                    condition = False
                    break
            
            atom2 = f.readline().split()
            
            for i in range(0, sortedList[2] - sortedList[1] - 1):
                try:
                    next(f)
                except:
                    condition = False
                    break
            
            atom3 = f.readline().split()
            
            for i in range(0, sortedList[3] - sortedList[2] - 1):
                try:
                    next(f)
                except:
                    condition = False
                    break
            
            atom4 = f.readline().split()
            # print(f.readline())
            
            if (len(atom1) == 0 or len(atom2) == 0 or len(atom3) == 0 or len(atom4) == 0):
                break
            
            # storing the selected coordinates as numpy arrays
            del atom1[0]
            atom1 = np.array(atom1, dtype='float')
            del atom2[0]
            atom2 = np.array(atom2, dtype='float')
            del atom3[0]
            atom3 = np.array(atom3, dtype='float')
            del atom4[0]
            atom4 = np.array(atom4, dtype='float')
            
            positionDict[sorted_keys[0]] = atom1  
            positionDict[sorted_keys[1]] = atom2   
            positionDict[sorted_keys[2]] = atom3   
            positionDict[sorted_keys[3]] = atom4   
             
            
            # Here I calculate the dihedral angle according to the initial order. How to do it?
            d.append(dihedral(positionDict["a1"], positionDict["a2"], positionDict["a3"], positionDict["a4"]))
        
            for i in range(0, nAtoms - sortedList[3] - 1):
                try:
                    next(f)
                except:
                    condition = False
                    break
                    
    d = np.array(d, dtype='float')
    return d
               
if __name__ == "__main__":               
    if len(sys.argv) != 9:
        print("Please, provide:")
        print("1) The starting coordinates")
        print("3) The two atoms that define the distance")
        print("4) The 4 atoms that define the dihedral angle")
        print("5) The output filename")
        exit(-1)
    
    try:
        positionFilename = sys.argv[1]
    
    # 1 based indices
        r1 = int(sys.argv[2])
        r2 = int(sys.argv[3])
        rr1 = int(sys.argv[4])
        rr2 = int(sys.argv[5])
        rr3 = int(sys.argv[6])
        rr4 = int(sys.argv[7])
        
        outputFilename = sys.argv[8]
    except TypeError:
        print("There is an error in parsing the provided information") 
        exit(-1)               
                
    t = timeCatcher(positionFilename)

    d = distanceCatcher(positionFilename, r1, r2)
# print(d)

    phi = dihedralCatcher(positionFilename, rr1, rr2, rr3, rr4)
# print(phi)

    # Visualization of the results with seaborn
    sns.set_style("whitegrid")
    sns.lineplot(x=t, y=d)
    plt.show()

    sns.lineplot(x=t, y=phi)
    plt.show()



    # Saving the output in the same directory of the trajectory
    path = positionFilename[:positionFilename.rfind('/')]

    savingOutput(path + outputFilename, time = t, distance = d, dihedral = d)
    # g = np.column_stack((t, d, phi))
    # np.savetxt(path + outputFilename, g, delimiter = ' ', header = "time/fs distance/A dihedral/deg", comments='')

