# README for Trajectory to XYZ Conversion Script
**Loknath Patro**  

---
## Overview

This script reads a molecular dynamics trajectory from XTC and topology from a GRO file, converts the coordinates from nanometers (nm) to angstroms (Å), and writes the data into an XYZ file format. The output file has a more compact format compared to the VMD-generated XYZ files. The main difference is that VMD generates extra space gaps (6-space gap between coordinates), while this script uses only a single space gap between coordinates, resulting in a smaller file size (half of vmd generated file).

## Requirements

* Python 3.x
* `mdtraj` library

  * To install it, you can use pip:

    ```
    pip install mdtraj
    ```

## Input Files

* **XTC file**: This file contains the molecular dynamics trajectory in XTC format.
* **GRO file**: This file contains the topology information for the trajectory.

Both files should be present in the same directory as the script.

## Output Files

* **output.xyz**: The script generates this output file in XYZ format. It includes the atom names and 3D coordinates in angstroms (Å), with one space gap between each value instead of the 6-space gap used by VMD.

## Example Command to Run

```bash
python xtc2xyz.py
```

## Conclusion

This script is an efficient way to convert molecular dynamics trajectory data to a compact XYZ format. It retains the precision and necessary information while reducing the file size compared to VMD-generated files.

