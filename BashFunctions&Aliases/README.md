# Bash Functions and Aliases for Lab Work

This repository contains a collection of useful **Bash functions** and **aliases** that simplify common tasks in the lab, such as generating plots from `.xvg` files, adjusting monitor brightness, debugging GaussView with GDB, and connecting to remote servers.

## Contents

1. **ConvertXVG2PNG**: Convert `.xvg` data files into PNG plots.
2. **brightness**: Adjust the brightness of all connected monitors.
3. **gaussview\_gdb**: Run GaussView within GDB for debugging.
4. **Aliases**: Shortcuts for SSH and SFTP connections.

---

## Prerequisites

* **Grace**: Used to generate PNG plots from `.xvg` files. Make sure it is installed and accessible.
* **xrandr**: Used to adjust the brightness of connected monitors.
* **GDB**: Used to run GaussView within a debugging environment.
* **EOG (Eye of GNOME)**: Used to display the generated PNG plot.

---

## Installation

To use these functions and aliases, simply add the contents of the `bashrc` script to your `.bashrc` file. Here's how:

1. Open your `.bashrc` file:

   ```bash
   nano ~/.bashrc
   ```

2. Copy and paste the functions and aliases into the file.

3. Save the file and reload your shell configuration:

   ```bash
   source ~/.bashrc
   ```

Now, you can use the functions and aliases in your terminal.

---

## Functions

### 1. `ConvertXVG2PNG`

This function converts `.xvg` files into PNG plots using the `grace` tool.

#### Usage:

```bash
ConvertXVG2PNG
```

* **Steps**:

  1. You will be prompted to enter the name of the `.xvg` file (make sure the file exists).
  2. The plot will be saved as a PNG file.
  3. The plot will open automatically in `eog` (Eye of GNOME).

---

### 2. `brightness`

This function adjusts the brightness of all connected monitors. The brightness is set to a value between 0 and 100.

#### Usage:

```bash
brightness <value (0-100)>
```

* **Example**:

```bash
brightness 50    # Set brightness to 50%
```

---

### 3. `gaussview_gdb`

This function runs GaussView within GDB, which is helpful for debugging and inspecting issues with GaussView.

#### Usage:

```bash
gaussview_gdb <path_to_input_file>
```

* **Example**:

```bash
gaussview_gdb input.gjf  # Run GaussView under GDB for debugging
```

---

## Aliases

### 1. `ssh_Gamma`

This alias allows you to SSH into the Gamma server with X11 forwarding.

#### Usage:

```bash
ssh_Gamma
```

* **Note**: Replace `user@ip` with the actual user and IP address for the Gamma server.

### 2. `sftp_Gamma`

This alias allows you to initiate an SFTP connection to the Gamma server.

#### Usage:

```bash
sftp_Gamma
```

* **Note**: Replace `user@ip` with the actual user and IP address for the Gamma server.

---

## Troubleshooting

1. **Grace not found**:
   If you get an error saying `grace: command not found`, you need to install Grace. On Ubuntu, use:

   ```bash
   sudo apt install grace
   ```

2. **GDB not found**:
   If GDB is not installed, you can install it on Ubuntu with:

   ```bash
   sudo apt install gdb
   ```

4. **GaussView not found**:
   If GaussView cannot be found, make sure the path to the executable (`/home/user/gv/gview.exe`) is correct. Update the script with the correct path if necessary.

---
