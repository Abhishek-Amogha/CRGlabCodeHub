# OPLS Force Field Compilation for GROMACS
**S. Abhishek**  

---

## Overview

This repository provides a comprehensive procedure for combining force field parameters for different molecules in molecular simulations using GROMACS. The process involves optimizing elemental structures, converting file formats, and compiling topology files. The included Python script assists in managing atom type numbering to avoid conflicts when merging topology files from different sources.

## Objectives

1. **Compile the necessary force field parameters into a single topology file (.top) for GROMACS.**

## Complete Procedure for Topology File Generation 

### Step 1: Optimizing Elemental Structures in Gaussian
- Optimize your molecular structures using Gaussian software.

### Step 2: Load Optimized .log Files in GaussView and Save as .pdb
- Load the optimized .log files in GaussView and save them as .pdb files.

### Step 3: Upload .pdb Files to LigParGen and Download .itp Files
- Go to the [LigParGen website](https://zarbi.chem.yale.edu/ligpargen/).
- Upload the .pdb files of A, B and C.
- Download the generated topology (.itp) and (.pdb) files.
- Note: Older .pdb files can be deleted after downloading the new ones from LigParGen.

### Step 4: Generate .top Topology File from Downloaded .itp Files
1. Create a new .top extention file and include the force field:
   ```plaintext
   #include "oplsaa.ff/forcefield.itp"
   ```
2. Include topology for ions at the end:
   ```plaintext
   #include "oplsaa.ff/ions.itp"
   ```
3. Append the downloaded .itp files (one for each molecule) into the .top file.
4. Modify the `[Atomtypes]` section:
   - Combine this section from all files into one, ensuring that atom type names do not overlap.
   - Use the provided Python script to find the maximum atom type number and start numbering the second one from a higher number. Perform the numbering for the third molecule's atoms in a similar manner.
   - Example command:
     ```bash
     python3 max_shift_TopologyFileGeneration.py
     ```
5. Modify the `[Atoms]` section:
   - Update atom names of each molecule to match the new atom-type numbers. The same python code will help you in achieving this.
   - Ensure the residue column matches the name mentioned under the `[moleculetype]` supersections.

### Finalize Topology File
- The final section of the .top file should look like this:
   ```plaintext
   [ system ]
   ; Name
   2A_2B_2C
   [ molecules ]
   ; Compound    	#mols
   A         	    100
   B           	    100
   C         	    1500
   ```
- Ensure that the order of molecules matches the order in the Packmol input file.

## Python Script: `max_shift_TopologyFileGeneration.py`

This script helps manage atom type numbering in topology files to avoid conflicts when combining force fields from different molecules. It provides two main functionalities:

1. **Find Maximum OPLS Number**: Identifies the highest atom type number in the provided data.
2. **Shift OPLS Numbers**: Adjusts atom type numbers to avoid overlaps when merging multiple topology files.

### Usage

1. Run the script:
   ```bash
   python3 max_shift_TopologyFileGeneration.py
   ```
2. Follow the prompts to either find the maximum OPLS number or shift OPLS numbers.

## Requirements

- Python 3.x

## Contributing

Contributions are welcome! If you have suggestions for improvements or additional features, feel free to open an issue or submit a pull request.
