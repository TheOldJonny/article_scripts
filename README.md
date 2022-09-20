**Introduction**
The code has been implemented by Jonathan Campeggio. For doubts and suggestions, please write an e-mail to *jonathan.campeggio@gmail.com*.

The Python files present in the folder can behave both like stand-alone scripts and modules. They can be imported with the statement
`import modulename`

in a user's Python file and the function called by the dot notazione 
`modulename.methodname(parameters)`

**Required libraries**
Provo a fare un file wheel per rendere il codice autocoerente
The code mainly relies on built-in Python libraries. The user has to install the following libraries to use the Python files:
1. `numpy`
2. `seaborn`
3. `matplotlib`

**Documentation**
*Preparator.py*
This program build a scan along the distance substrate-surface. In particular, it generates a series of folders each of them containing the CP2K input file and the coordinates. 
To use it, use the terminal command inside the folder where there is the script
`python3 Preparator.py positions.xyz NAtoms z0 input.inp output.out`

Where:

1. `positions.xyz` is the file that contains the starting `xyz` coordinates. The coordinates are expressed in &#8491;. 
2. `NAtoms` is the number of atoms of the substrate.
3. `z0` is the *z* coordinate of the nearest substrate atom to the surface.
4. `input.inp` is the input file (in the present article is the CP2K input)
5. `output.out` is the name of the output `xyz` coordinates to be stored in each folder.

The code's aim is to describe the neighborhood of `z0`. The interval is `[z0 - 1` &#8491; , `z0 + 6` &#8491;`]`. The grid has a tighter spacing of $0.1$ &#8491; in the range $[z-0.5 $ &#8491;$, z+0.5 $ &#8491;$]$, then the spacing becomes broader. 
The variable `relativeDisplacements` can be edited to modify this grid.

*TrajectoryAnalyzer.py*
This code is useful to handle a trajectory coordinates file. It can be used both as a standalone script and as a module.
The user can use the following command to use the script:
`python3 TrajectoryAnalyzer.py trajectory.xyz atom1 atom2 atmo3 atom4 atom5 atom6 output.out`

Where:
1. `trajectory.xyz` is the `xyz` trajectory file
2. `atom1` and `atom2` are the indices ($1$-based integers) that describe the bond distance
3. `atom3 atom4 atom5 atom6` are the indices ($1$-based integers) that describe the dihedral angle
4. `output.out` the name of the output file.

A user can find more interesting the usage as a module. After the importing (`import TrajectoryAnalyzer.py`), the user can use the implemented function to analyze a general trajectory.

For example, the function `timeCatcher(trajectory.xyz)` reads the trajectory and it stores the time in a `numpy` array. The most flexible function in the module is `savingOutput(filename, **kwargs)`. It concatenates the `numpy` arrays given in iput as keyword arguments and it saves in the `filename` file. Along with the $3$ catcher functions (`distanceCatcher`, `angleCatcher`, and `dihedralCatcher`), it allows the user to completely analyze the trajectory trends of bond distances, bond angles, and dihedral angles.

 The code is extensively commented on, and it extensively uses type hints.


*Launcher.py*
As in the publication, one can have to analyze a series of trajectories. *Launcher.py* performs the same operation of the previous code, but for all the folders in a given path. The command is:
`python3 Launcher.py path trajectory.xyz atom1 atom2 atmo3 atom4 atom5 atom6 output.out`

where `path` is the path where all the folders containing the `trajectory.xyz` files are stored.

