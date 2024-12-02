import os
import pandas as pd

# Function to combine all Excel files in a folder
def combine_excel_files(input_folder, output_file):
    # List to store dataframes
    dfs = []

    # Iterate through all files in the specified folder
    for filename in os.listdir(input_folder):
        if filename.endswith('.xlsx'):
            file_path = os.path.join(input_folder, filename)
            print(f"Reading file: {file_path}")

            # Read the Excel file into a pandas dataframe
            df = pd.read_excel(file_path)

            # Append dataframe to list
            dfs.append(df)

    # Concatenate all dataframes vertically (row-wise)
    combined_df = pd.concat(dfs, ignore_index=True)

    # Write the grouped dataframe to a new Excel file
    combined_df.to_excel(output_file, index=False)
    print(f"Grouped data saved to: {output_file}")

# Main entry point
if __name__ == '__main__':
    # Set the folder containing Excel files and the output file name
    input_folder = 'data/GPT/'  # Replace with the folder path
    output_file = 'data/GPT/combined.xlsx'  # Output file name

    combine_excel_files(input_folder, output_file)
