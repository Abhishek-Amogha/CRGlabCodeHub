import os

def check_file_existence(file_path):
    return os.path.isfile(file_path)

def save_script(queue, nodes):
    JOB_NAME = input("\nEnter the job name: ").strip()
    MDP_DIR = "{MDP_DIR}"
    OUTPUT_DIR = "{OUTPUT_DIR}"
    topScript = f"""#!/bin/bash
#PBS -N {JOB_NAME}
#PBS -o out.log
#PBS -e err.log
"""
    testTopScript = f"""#!/bin/bash
#PBS -N test_{JOB_NAME}
#PBS -o out.log
#PBS -e err.log
"""

    # Initialize script content
    # for test Script file, in serial node
    procsPerNode = 1
    testTopScript += f"""#PBS -l nodes=1:ppn={procsPerNode}
#PBS -j oe
#PBS -q serial

"""
    
    # for Actual Script
    procsPerNode = 32
    topScript += f"""#PBS -l nodes={nodes}:ppn={procsPerNode}
#PBS -j oe
#PBS -q {queue}

"""
    
    mainScript = f"""#echo job related information in job output file
echo "PBS JOB id is $PBS_JOBID"
NPROCS=$(wc -l < $PBS_NODEFILE)
echo "NPROCS is $NPROCS"

# go inside job submission dir
cd $PBS_O_WORKDIR

module load compilers/intel/OneAPI/2021.1
module load codes/intel/gromacs/2024.2

#create nodes file contating execution nodenames
cat $PBS_NODEFILE | sort | uniq > nodes

NP=`cat $PBS_NODEFILE|wc -l`
"""
    # Calculate TOTAL_PROCS
    if queue == "serial":
        TOTAL_PROCS = nodes * 1
    else:
        while True:
            max_procs = nodes * 32
            min_procs = (nodes - 1) * 32 + 1
            TOTAL_PROCS = int(input("How many procs do u wanna use: "))
            if min_procs <= TOTAL_PROCS <= max_procs:
                break
            else:
                print(f"Please enter a number between {min_procs} and {max_procs}.\n")
    
    mainScript += f"""
# Define variables | Change asper your needs
TOPFILE="topol.top"  # ur topology file
MDP_DIR="{MDP_DIR}"     # Directory with .mdp files
OUTPUT_DIR="{OUTPUT_DIR}"             # Directory for output files
TOTAL_PROCS="{TOTAL_PROCS}"

"""
    TOTAL_PROCS = "{TOTAL_PROCS}"
    mainScript += f"""
# Create output directory
mkdir -p $OUTPUT_DIR
echo "Created output directory: $OUTPUT_DIR"

"""

    # Ask if em should be carried out
    perform_em = input("Wanna perform Energy Minimization? (yes / y / other for 'no'): ").strip().lower() in ["yes", "y"]
    if perform_em:
        # Define the default directory and expected PDB file extension
        default_directory = "Step2Pack"

        # Get user input for the PDB file
        input_pdb_file = input(f"Enter the name of the PDB file (located in '{default_directory}'): ").strip()
        full_file_path = os.path.join(default_directory, f"{input_pdb_file}")

        # Check if the file exists
        if not check_file_existence(full_file_path):
            print(f"\nFile '{full_file_path}' does not exist. Please check the filename and try again.")
            return

        print(f"File '{full_file_path}' found.\n")
    
        mainScript += f"""INPUT_PDB_FILE="Step2Pack/{input_pdb_file}"  # Input coordinates file
# Energy Minimization
echo "Starting Energy Minimization..."
gmx_mpi grompp -f ${MDP_DIR}/minim.mdp -c $INPUT_PDB_FILE -r $INPUT_PDB_FILE -p $TOPFILE -o ${OUTPUT_DIR}/em.tpr
mpiexec -np ${TOTAL_PROCS} gmx_mpi mdrun -v -deffnm ${OUTPUT_DIR}/em

# Create folder for Energy Minimization files and move them
mkdir -p ${OUTPUT_DIR}/Step4EnergyMinimisation
echo "Created directory for Energy Minimization files: $OUTPUT_DIR/Step4EnergyMinimisation"
cp ${OUTPUT_DIR}/em* ${OUTPUT_DIR}/Step4EnergyMinimisation/
echo "Copied Energy Minimization files to $OUTPUT_DIR/Step4EnergyMinimisation/"
cp mdout.mdp ${OUTPUT_DIR}/Step4EnergyMinimisation/ 2>/dev/null
echo "Copied mdout.mdp to $OUTPUT_DIR/Step4EnergyMinimisation/"

"""

# Ask if NPT 1 should be carried out
    wannaPerformNPTs = input("Wanna perform any NPT? (yes / y / other for 'no'): ").strip().lower() in ["yes", "y"]
    if wannaPerformNPTs:
        perform_npt1 = input("Wanna perform NPT Equilibration 1? (yes / y / other for 'no'): ").strip().lower() in ["yes", "y"]
        
        start_npt = -1
        end_npt = -1
    
        if perform_npt1:
            mainScript += f"""# Equilibration (NPT 1)
echo "Starting NPT Equilibration 1..."
gmx_mpi grompp -f ${MDP_DIR}/npt.mdp -c ${OUTPUT_DIR}/em.gro -r ${OUTPUT_DIR}/em.gro -p $TOPFILE -o ${OUTPUT_DIR}/npt_1.tpr -maxwarn 1
mpiexec -np ${TOTAL_PROCS} gmx_mpi mdrun -deffnm ${OUTPUT_DIR}/npt_1 -cpi ${OUTPUT_DIR}/npt_1.cpt -v > gmx.out

# Create folder for NPT 1 files and move them
mkdir -p ${OUTPUT_DIR}/Step5.1NPT
echo "Created directory for NPT 1 files: $OUTPUT_DIR/Step5.1NPT"
cp ${OUTPUT_DIR}/npt* ${OUTPUT_DIR}/Step5.1NPT/
echo "Copied NPT 1 files to $OUTPUT_DIR/Step5.1NPT/"
cp mdout.mdp ${OUTPUT_DIR}/Step5.1NPT/ 2>/dev/null
echo "Copied mdout.mdp to $OUTPUT_DIR/Step5.1NPT/"

"""

            # Ask for the number of NPT equilibration steps
            while True:
                try:
                    wannaDoMoreNPTs = input("Wanna perform more NPTs? (yes / y / other for 'no'): ").strip().lower() in ["yes", "y"]
                    if wannaDoMoreNPTs:
                        num_npts = int(input("How many total NPT equilibration steps do u wanna perform (npt_1 is done): "))
                        if num_npts > 1:
                            start_npt = 2
                            end_npt = num_npts
                            break
                        else:
                            print("Please enter a number greater than 1. Bcoz u wanted to perform more than npt_1")
                    else:
                        end_npt = 1
                        break
                except ValueError:
                    print("Invalid input. Please enter a number.")
                    
        if not perform_npt1:
            # Ask for the NPT equilibration steps
            while True:
                try:
                    start_npt = int(input("Which NPT equilibration step do u like to start with: "))
                    end_npt = int(input("Which NPT equilibration step do u like to end with: "))
                    break
                except ValueError:
                    print("Invalid input. Please enter a number.")

        if start_npt > 0 and end_npt >= start_npt:
            # Add further NPTs if requested
            for i in range(start_npt, end_npt + 1):
                mainScript += f"""# Equilibration (NPT {i}) 
echo "Starting NPT Equilibration {i}..."
gmx_mpi grompp -f ${MDP_DIR}/npt_{i}.mdp -c ${OUTPUT_DIR}/npt_{i-1}.gro -r ${OUTPUT_DIR}/npt_{i-1}.gro -p $TOPFILE -o ${OUTPUT_DIR}/npt_{i}.tpr
mpiexec -np ${TOTAL_PROCS} gmx_mpi mdrun -deffnm ${OUTPUT_DIR}/npt_{i} -cpi ${OUTPUT_DIR}/npt_{i}.cpt -v > gmx.out

# Create folder for NPT {i} files and move them
mkdir -p ${OUTPUT_DIR}/Step5.{i}NPT_{i}
echo "Created directory for NPT {i} files: $OUTPUT_DIR/Step5.{i}NPT_{i}"
cp ${OUTPUT_DIR}/npt_{i}* ${OUTPUT_DIR}/Step5.{i}NPT_{i}/
echo "Copied NPT {i} files to $OUTPUT_DIR/Step5.{i}NPT_{i}/"
cp mdout.mdp ${OUTPUT_DIR}/Step5.{i}NPT_{i}/ 2>/dev/null
echo "Copied mdout.mdp to $OUTPUT_DIR/Step5.{i}NPT_{i}/"

"""

    # Ask if the user wants to perform the production run
    perform_production = input("Wanna perform a production run? (yes / y / other for 'no'): ").strip().lower() in ["yes", "y"]

    # Production Run
    if perform_production:
        if not wannaPerformNPTs:
            # If NPT's were not performed, ask for the last NPT done
            while True:
                try:
                    end_npt = int(input("Which was the last NPT equilibration step that was completed: "))
                    if end_npt >= 1:
                        break
                    else:
                        print("Please enter a number >= 1")
                except ValueError:
                    print("Invalid input. Please enter a number.")
            
        mainScript += f"""# Production Run
echo "Starting Production Run..."
gmx_mpi grompp -f ${MDP_DIR}/md.mdp -c ${OUTPUT_DIR}/npt_{end_npt}.gro -p $TOPFILE -o ${OUTPUT_DIR}/md_0_1.tpr
mpiexec -np ${TOTAL_PROCS} gmx_mpi mdrun -deffnm ${OUTPUT_DIR}/md_0_1 -cpi ${OUTPUT_DIR}/md_0_1.cpt -v > gmx.out

# Move production files to Step 6 folder
mkdir -p ${OUTPUT_DIR}/Step6ProductionRun
echo "Created directory for production run files: $OUTPUT_DIR/Step6ProductionRun"
cp ${OUTPUT_DIR}/md_0_1* ${OUTPUT_DIR}/Step6ProductionRun/
echo "Copied production run files to $OUTPUT_DIR/Step6ProductionRun/"
cp mdout.mdp ${OUTPUT_DIR}/Step6ProductionRun/ 2>/dev/null
echo "Copied mdout.mdp to $OUTPUT_DIR/Step6ProductionRun/"

"""

    mainScript += """echo "All steps completed!"

# add -append at the end to to continue from a particular step.
#to submit serial job use qsub <submitfile >
#to see the echoed infos, check out.log file
#to see the current step of the currently running command, check the repective log file, using the below example
# tail -f ${OUTPUT_DIR}/md_0_1.log
"""

    # Save to a shell script file
    file_name = JOB_NAME + ".run"
    with open(file_name, "w") as script_file:
        script_file.write(topScript + mainScript)
        print("\nAutomation script saved -> ", file_name)
    
    # Save a test script file, on serial node
    file_name = "test_" + JOB_NAME + ".run"
    with open(file_name, "w") as test_file:
        test_file.write(testTopScript + mainScript)
        print("Test script saved ->       ", file_name)
        
    print("\nEnsure: \n 1. All mdp files are present in the '", MDP_DIR, "' specified in the script.\n  2. topol.top file is in the current directory, and\n    3. pre-requisite files like npt_n.gro/em.gro files are moved to the '",  OUTPUT_DIR, "' directory specified in the script.")

def main():  
    print("===== Hartree Classical MD Job File Generator =====")
    # Prompt user for the type of node
    print("\nSelect the type of node:")
    print("1. Short (12 hours, 1-2 nodes)")
    print("2. Medium (48 hours, 1-11 nodes)")
    print("3. Long (168 hours, 1-21 nodes)")

    while True:
        node_choice = input("Enter the number corresponding to ur choice (1/2/3): ").strip()
        if node_choice in ['1', '2', '3']:
            break
        else:
            print("Invalid input. Please enter 1, 2, or 3.")

    # Set parameters based on the choice
    if node_choice == '1':
        queue = "short"
        max_nodes = 2
    elif node_choice == '2':
        queue = "medium"
        max_nodes = 4
    elif node_choice == '3':
        queue = "long"
        max_nodes = 4

    # Ask for the number of nodes to use
    while True:
        nodes = input(f"How many nodes do u wanna use (1-{max_nodes})? ").strip()
        try:
            nodes = int(nodes)
            if 1 <= nodes <= max_nodes:
                break
            else:
                print(f"Please enter a number between 1 and {max_nodes}.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    # Save the automation script based on user input
    save_script(queue, nodes)
    
if __name__ == "__main__":
    main()
