# Packmol Isomer Handling / Renaming
**S. Abhishek**  

---

## Overview

This repository provides a procedure for creating initial configurations of molecules in a simulation box using Packmol, with a focus on handling different structural isomers. The included Python script automates the renaming of isomers after packing to ensure continuity and proper integration in molecular simulations.

## Objectives

1. **Create initial configurations of molecules in a simulation box using Packmol.**
2. **Handle different structural isomers to ensure proper integration and avoid overlaps.**
3. **Automate the renaming of isomers after packing to maintain continuity.**

## Key Considerations

### Normalization Steps
- Small adjustments are necessary for easy system preparation.
- Carefully consider the arrangement of isomers to avoid overlaps and ensure correct packing and easy manipulation of the topology file.

### Input File Organization
For clarity, list all isomers consecutively in the input file. Recommended placement is either at the top or at the bottom of the file. Here’s an example format:

```plaintext
# Other input parameters
…
# Molecules definitions
structure A.pdb
  number 999
  inside cube 0. 0. 0. 120.
end structure

structure B.pdb
  number 999
  inside cube 0. 0. 0. 120.
end structure

# Isomers definitions
structure C.pdb
  number 1248
  inside cube 0. 0. 0. 120.
end structure
 
structure C_conformer2.pdb
  number 1248
  inside cube 0. 0. 0. 120.
end structure

structure C_conformer3.pdb
  number 500
  inside cube 0. 0. 0. 120.
end structure

structure C_conformer4.pdb
  number 500
  inside cube 0. 0. 0. 120.
end structure
```

### Processing the Packed File
After packing, each isomer may be treated as a separate molecule. You need to rename them to maintain continuity. For example, if you have packed 1250 molecules of C and the next line states D 1, change it to C 1251. Repeat this for all isomers (D, E, F). The final naming should reflect cumulative counts, ending with C{total count} for the last isomer.

## Python Script: `IsomerRenamerPackmol.py`

This script automates the renaming of isomers in the packed file. It prompts the user for input and generates updated lines for the packed file.

### Functionality of the Script
- Prompts the user for:
  - Input lines (copy from any text-editor and paste)
  - Isomers to be replaced (e.g., C_conformer2 C_conformer3 C_conformer4)
  - Replacement letter (e.g., C)
  - Last value of the replacement series (to determine the total count for renaming)

### Usage

1. Run the script:
   ```bash
   python3 IsomerRenamerPackmol.py
   ```
2. Follow the prompts to enter the input lines, target letters, replacement letter, and the last value of the replacement series.
3. The script will generate updated lines and write them to a file named `delete_ForCopy.pdb`.

## Requirements

- Python 3.x
- Basic knowledge of molecular dynamics and Packmol.

## Contributing

Contributions are welcome! If you have suggestions for improvements or additional features, feel free to open an issue or submit a pull request.
