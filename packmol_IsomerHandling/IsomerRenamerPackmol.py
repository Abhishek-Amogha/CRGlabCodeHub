import re

def update_series(input_lines, target_letters, replacement_letter):
    updated_lines = []
    # Ask for the initial current C series
    current_c_series = int(input(f"Enter the last value of the {replacement_letter} series (e.g., 1249): "))
    last_number = None  # To keep track of the last number

    # Create a pattern for the target letters
    pattern = r"(\s*|^)([" + "".join(target_letters) + r"])(\s*)(\d+)(\s*|$)"

    for line in input_lines:
        match = re.search(pattern, line)
        
        if match:
            series_number = int(match.group(4))  # The number after the letter
            
            if last_number is None or series_number != last_number:
                current_c_series += 1  # Increment C series if the number changes
                last_number = series_number
            
            # Replace the target series with the replacement letter and current C series
            # Check if the series number is 1000 or more
            if current_c_series >= 1000:
                updated_line = line.replace(f"{match.group(2)}{match.group(3)}{match.group(4)}", f"{replacement_letter}{current_c_series}")
            else:
                updated_line = line.replace(f"{match.group(2)}{match.group(3)}{match.group(4)}", f"{replacement_letter} {current_c_series}")
            
            updated_lines.append(updated_line)
        else:
            updated_lines.append(line)  # Keep the line unchanged

    return updated_lines

# Get input lines from the user
print("Enter the lines (empty line to finish):")
input_lines = []
while True:
    line = input()
    if line == "":
        break
    input_lines.append(line)

# Ask for multiple target letters
target_letters = input("Enter the letters (e.g., D E F) to be replaced: ").replace(" ", "")
# Ask for the replacement letter
replacement_letter = input("Enter the replacement letter: ")

# Update the series
updated_lines = update_series(input_lines, target_letters, replacement_letter)

# Print the updated output
#for line in updated_lines:
#    print(line)

# Write the updated output to a file
with open("delete_ForCopy.pdb", "w") as output_file:
    for line in updated_lines:
        output_file.write(line + "\n")

print("Output written to delete_ForCopy.pdb")
