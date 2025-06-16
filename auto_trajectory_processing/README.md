# GROMACS Trajectory Processing Automation
**S. Abhishek**  

---

## Overview

This repository contains an Expect script designed to automate the processing of GROMACS trajectory files using the `gmx trjconv` command. The core principle of this script is: **"Configure your file saving method once, automate forever."** With this setup, you can efficiently manage and convert multiple trajectory files with minimal manual intervention.

### What Does the Code Do?

The script leverages `gmx trjconv` to perform various operations on molecular dynamics trajectory files, including:

- **File Format Conversion:** Convert trajectory files between formats such as `.xtc`, `.trr`, `.gro`, `.g96`, `.pdb`, and `.tng`.
- **Atom Selection:** Specify which atoms to include in the output trajectory for targeted analysis.
- **Periodic Boundary Condition Handling:** Properly treat periodic boundaries to keep molecules intact.
- **Centering and Fitting:** Center trajectories or fit structures as needed.

### What Can You Easily Tweak?

- **Frame Reduction:** Reduce the number of frames in the output to save disk space and simplify analysis.
- **File Paths & Names:** Modify the list of trajectory files and output names in the configuration section.
- **Selection Settings:** Adjust atom groups and other `gmx trjconv` options to suit your analysis needs.

## Features

- **Easy Configuration:** Modify file paths and output settings in one centralized location.
- **Automated Processing:** The script handles trajectory conversion automatically, minimizing manual commands.
- **Scalable:** Add more trajectory files easily without changing core logic.

## Requirements

- GROMACS installed on your system.
- Expect installed (`apt-get install expect` or equivalent).
- Basic command-line knowledge.

## Usage

1. **Clone the Repository / Download the Script**

2. **Configure the Script:**  
Open the script file and modify the **configuration section** at the top to specify your trajectory files and desired output settings.

```tcl
set traj_files {
    {Step5.2NPT_2/npt_2.trr Step5.2NPT_2/npt_2.tpr Step5.2NPT_2/npt_2.xtc}
    {Step5.3NPT_3/npt_3.trr Step5.3NPT_3/npt_3.tpr Step5.3NPT_3/npt_3.xtc}
    # Add more trajectory files as needed
}

set final_traj {
    Step6ProductionRun/md_0_1.tpr Step6ProductionRun/md_0_1.xtc Step6ProductionRun/md_0_1_ByCommand.xtc
}
```

3. **Execute the Script:**

```bash
chmod +x auto_traj_v2.sh
./auto_traj_v2.sh
```

4. **Check Notifications:**  
Once processing completes, you'll receive a desktop notification indicating success. Check the terminal for any errors or issues.


## Contributing

Contributions are welcome! If you have suggestions, bug reports, or feature requests, please open an issue or submit a pull request. Your feedback helps improve this automation tool.
