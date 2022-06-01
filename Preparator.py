import math
import os
import sys
import subprocess
import shutil

relativeDisplacements = [-1, -0.5, -0.4, -0.3, -0.2, -0.1, 0.1, 0.2, 0.3, 0.4, 0.5, 1., 2., 4., 6.]


# This function uses an awk command to translate the substrate
# in a xyz file along the z axis respect the equilibrium position
def command(*,
            NAtoms : int,
            relativeDistance : float,
            coordinates : str, 
            output : str) -> None:
    cmd = "awk '{ if (NR > 2 && NR < " + str(int(3 + NAtoms)) + ") {$4+="+str(relativeDistance)+"} print}' " + coordinates +"> " + output
    try:
        subprocess.call(cmd, shell=True)
    except OSError:
        print("The awk call has failed. Please control the input points")
    
    return None

# This function creates the scan on the distance starting from the equilibrium value
# It calls the function command inside and insert the xyz new coordinates in the folder 
def folderBuilder(*, deq : float,
                  scanList : list,
                  cp2kInput : str,
                  NAtoms : int,
                  coordinates : str,
                  output : str,
                  cinecaInput = "Launcher.slr") -> None:
    for i in scanList:
        filename = str(deq + i)
        try:
            os.mkdir(filename)
            command(NAtoms = NAtoms, relativeDistance = i, coordinates = coordinates, output=filename + "/" + output )
            subprocess.call("cp " + cp2kInput + " " + filename + "/", shell = True)
            subprocess.call("cp  acyl-RESTART.wfn " + filename + "/", shell = True)
            subprocess.call("cp " + cinecaInput + " " + filename + "/", shell = True)
        except FileExistsError:
            shutil.rmtree(filename)
            os.mkdir(filename)
            command(NAtoms = NAtoms, relativeDistance = i, coordinates = coordinates, output=filename + "/" + output )
            subprocess.call("cp " + cp2kInput + " " + filename + "/", shell = True)
            subprocess.call("cp  acyl-RESTART.wfn " + filename + "/", shell = True)
            subprocess.call("cp " + cinecaInput + " " + filename + "/", shell = True)




if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Please, provide:")
        print("1) The starting coordinates")
        print("2) The number of atoms for the substrate")
        print("3) The equilibrium z component of the nearest substrate atom to the surface")
        print("4) The cp2k input filename")
        print("5) The output name")
        exit(-1)
    

    try:
        coordinates = sys.argv[1]
        NAtoms = int(sys.argv[2])
        equilibriumDistance = float(sys.argv[3])
        cp2kInput = sys.argv[4]
        output = sys.argv[5]
    except TypeError:
        print("There is an error in parsing the provided information")
	exit(-1)


    folderBuilder(deq = equilibriumDistance, scanList= relativeDisplacements, cp2kInput=cp2kInput, NAtoms = NAtoms, coordinates=coordinates, output=output)



