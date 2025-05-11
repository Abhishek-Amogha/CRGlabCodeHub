import mdtraj as md

# Load trajectory from GRO and XTC files (coordinates in nm)
traj = md.load('file.xtc', top='file.gro')

# Prepare a list of atom names from the topology
atom_names = [atom.name for atom in traj.topology.atoms]

# Open the output file for writing
with open("output.xyz", "w") as outfile:
    n_atoms = traj.n_atoms
    # Iterate over each frame in the trajectory
    for frame in traj.xyz:
        # Write the number of atoms
        outfile.write(f"{n_atoms}\n")
        # Write the header line
        outfile.write("Created by MDTraj\n")
        # Convert coordinates from nm to angstroms (1 nm = 10 angstroms)
        for i, coord in enumerate(frame * 10):
            outfile.write(f"{atom_names[i]} {coord[0]:.6f} {coord[1]:.6f} {coord[2]:.6f}\n")

print("Conversion to XYZ format completed with 6-digit precision and unit conversion to angstroms!")
