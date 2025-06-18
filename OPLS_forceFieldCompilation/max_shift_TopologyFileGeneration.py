import re

def find_max_opls_number(data):
    """Function to find the maximum number (b) in the opls_ labels"""
    max_number = 0
    pattern = r'opls_(\d+)'
    
    for line in data:
        match = re.search(pattern, line)
        if match:
            num = int(match.group(1))
            if num > max_number:
                max_number = num
                
    return max_number

def shift_opls_numbers(data, new_start, change_repeating_numbers):
    """Function to shift opls numbers and optionally the corresponding repeating numbers"""
    min_num = min(int(re.search(r'opls_(\d+)', line).group(1)) for line in data)
    shifted_data = []
    
    for line in data:
        match = re.search(r'opls_(\d+)', line)
        if match:
            original_number = int(match.group(1))
            new_number = original_number - min_num + new_start
            
            # Update the opls_ number
            shifted_line = re.sub(r'opls_(\d+)', f'opls_{new_number:03}', line)
            
            # Optionally update the repeating number that follows a letter
            if change_repeating_numbers:
                shifted_line = re.sub(r'([A-Z])(\d+)', lambda m: f"{m.group(1)}{new_number:03}", shifted_line)
            
            shifted_data.append(shifted_line)
            
    return shifted_data

def main():
    while True:
        # Ask user what they want to do
        action = input("Enter 'max' to find the maximum opls number, 'shift' to shift opls numbers, or 'exit' to quit: ").strip().lower()

        if action == 'exit':
            print("Exiting the program. Goodbye!")
            break

        elif action == 'max':
            # User will paste the data
            print("Please paste your data (end with an empty line):")
            lines = []
            while True:
                line = input()
                if line.strip() == "":
                    break
                lines.append(line)
            
            # Find and print the maximum opls number
            max_opls_number = find_max_opls_number(lines)
            print(f"The maximum opls number is: {max_opls_number}")

        elif action == 'shift':
            # User will paste the data
            print("Please paste your data (end with an empty line):")
            lines = []
            while True:
                line = input()
                if line.strip() == "":
                    break
                lines.append(line)
            
            # Ask for the new starting point
            new_start = int(input("Enter the new starting number (e.g., 0 for 000, 100 for 100): ").strip())

            # Ask if the user wants to change the numbers following the letters
            change_repeating_numbers = input("Do you want to change the numbers following the letters (yes/no)? ").strip().lower() == 'yes'
            
            # Perform the shift
            shifted_data = shift_opls_numbers(lines, new_start, change_repeating_numbers)
            
            # Print the shifted data
            print("\nShifted opls numbers:")
            for line in shifted_data:
                print(line)
        else:
            print("Invalid input. Please try again.")

if __name__ == "__main__":
    main()

