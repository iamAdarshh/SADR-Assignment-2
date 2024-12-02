import os

def extract_part_from_string(input_string):
    # Replace backslashes with forward slashes to standardize the path
    input_string = input_string.replace("\\", "/")
    # Extract the part of the string after the last slash
    file_name = os.path.basename(input_string)
    # Remove the file extension and return the result
    return file_name.split('.')[0]

# Example strings
string1 = "/Users/adarshchoudhary/Documents/University of Paderborn/Software Architecture Design and Recovery/Assignment 2/code/data/archi/axis\\TxtTacticFiles\\ActiveRedundancy.txt"
string2 = "/archi/axis\\TxtTacticFiles\\ActiveRedundancy.txt"

# Extract the part from both strings
part1 = extract_part_from_string(string1)
part2 = extract_part_from_string(string2)

print(part1)  # Output: ActiveRedundancy
print(part2)  # Output: ActiveRedundancy
