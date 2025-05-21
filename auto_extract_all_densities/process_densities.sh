#!/usr/bin/env expect
set timeout -1

# Define the target directory
set target_dir "InfoDensity"

# Create the directory if it does not exist
file mkdir $target_dir

# Function to recursively find all .edr files using the find command
proc find_edr_files {} {
    # Use the 'find' command to search for .edr files, using /bin/sh to execute
    set cmd "find . -type f -name '*.edr'"

    # Run the 'find' command and capture the output
    set edr_files [exec /bin/sh -c $cmd]

    return $edr_files
}

# Get all .edr files recursively
set edr_files [find_edr_files]

# Loop through each .edr file
foreach edr_file $edr_files {
    # Skip files named em.edr (energy minimization steps)
    if {[file tail $edr_file] eq "em.edr"} {
        puts "Skipping $edr_file (Energy Minimization)"
        continue
    }

    # Extract base filename for output file name
    set output_file [string map {".edr" ""} $edr_file]
    append output_file "_density.xvg"

    # Spawn gmx energy for each .edr file
    puts "Processing $edr_file ..."
    spawn gmx energy -f $edr_file -o $output_file
    expect "End your selection with an empty line or a zero"
    send "Density\r\r"
    expect eof

    # Move the output file to the target directory
    exec mv $output_file $target_dir
    puts "Moved file: $output_file"
}

# Notify when all files are processed
exec notify-send -u critical "Density Calculation Complete!" "All densities have been calculated! Check the terminal for potential errors"

