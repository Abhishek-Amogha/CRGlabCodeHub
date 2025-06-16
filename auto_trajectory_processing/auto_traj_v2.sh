#!/usr/bin/env expect
set timeout -1

# Configuration section: Modify these variables as needed
# List of trajectory files: each element is a list {trr_file tpr_file xtc_file}
set traj_files {
    {Step5.2NPT_2/npt_2.trr Step5.2NPT_2/npt_2.tpr Step5.2NPT_2/npt_2.xtc}
    {Step5.3NPT_3/npt_3.trr Step5.3NPT_3/npt_3.tpr Step5.3NPT_3/npt_3.xtc}
}
    # Add more trajectory files as needed
    # {Step5.4NPT_4/npt_4.trr Step5.4NPT_4/npt_4.tpr Step5.4NPT_4/npt_4.xtc}

set final_traj {
    Step6ProductionRun/md_0_1.tpr Step6ProductionRun/md_0_1.xtc Step6ProductionRun/md_0_1_ByCommand.xtc
}

# Function to process trajectory files
proc process_trajectory {trr_file tpr_file xtc_file} {
    spawn gmx trjconv -f $trr_file -s $tpr_file -o $xtc_file -pbc mol -center
    expect "Select a group:"
    send "0\r"  ; # Adjust this based on your actual input. 0 stands for 'System'
    expect "Select a group:"
    send "0\r"  ; # Adjust this based on your actual input. 0 stands for 'System'

    # Expect various completion messages
    expect {
        -re "Last frame" {
            # Successfully captured the end of the process
        }
        -re "GROMACS reminds you:" {
            # Successfully captured the GROMACS reminder. Truly signifies the end of the process without any error.
        }
        timeout {
            puts "Process timed out for $trr_file."
            exit 1
        }
        default {
            puts "Unexpected output for $trr_file: $expect_out(buffer)"
            exit 1
        }
    }

    # Ensure we reach eof before proceeding
    expect eof 
}

# Process each trajectory file
foreach traj $traj_files {
    set trr_file [lindex $traj 0]
    set tpr_file [lindex $traj 1]
    set xtc_file [lindex $traj 2]
    process_trajectory $trr_file $tpr_file $xtc_file
}

# Process the final trajectory
set final_trr_file [lindex $final_traj 1]
set final_tpr_file [lindex $final_traj 0]
set final_xtc_file [lindex $final_traj 2]
process_trajectory $final_trr_file $final_tpr_file $final_xtc_file

# Use exec to call notify-send
exec notify-send -u critical "I Made All Trajectories!" "All trajectories have been made! Check the terminal for potential errors"
