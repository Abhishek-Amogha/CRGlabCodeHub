# Hartree Classical MD Job File Generator
**S. Abhishek**  

---

## Introduction

This script generates job files for Classical MD Simulations using GROMACS on a high-performance computing (HPC) cluster. The script prompts the user for input and creates a job file based on their selections.

## Features

* Generates job files for GROMACS simulations
* Supports different types of nodes (short, medium, long) with varying time limits and node counts
* Allows users to specify the number of nodes to use
* Includes options for energy minimization, NPT equilibration, and production runs
* Creates a test script file for serial nodes

## Usage

1. Run the script and select the type of node you want to use:
	* Short (12 hours, 1-2 nodes)
	* Medium (48 hours, 1-11 nodes)
	* Long (168 hours, 1-21 nodes)
2. Enter the number of nodes you want to use (within the limits for your chosen node type)
3. Follow the prompts to specify your job name, energy minimization, NPT equilibration, and production run options
4. The script will generate a job file (`.run` file) and a test script file (`.run` file with `test_` prefix)

## Requirements

* GROMACS installed on the HPC cluster
* `mdp` files present in the specified directory
* `topol.top` file present in the current directory
* Pre-requisite files (e.g., `npt_n.gro`, `em.gro`) moved to the specified output directory

## Notes

* Ensure that all required files are present in the correct directories before submitting the job
* Check the output directory for the generated job files and test script file
* Use the `qsub` command to submit the job file to the HPC cluster

## Example Use Case

1. Run the script and select the "medium" node type
2. Enter 2 nodes to use
3. Specify your job name, energy minimization, and NPT equilibration options
4. The script generates a job file (`my_job.run`) and a test script file (`test_my_job.run`)
5. Submit the job file to the HPC cluster using `qsub my_job.run`
