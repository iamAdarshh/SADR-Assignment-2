import pandas as pd
import re

# Load the data from the Excel file
file_path = 'data/GPT/combined.xlsx'  # Replace with the actual file path
data = pd.read_excel(file_path)

# Function to replace patterns like "nan, nan, nan, ..." with None
def replace_nan_values_with_none(df):
    # Iterate over each column
    for column in df.columns:
        # Replace patterns of "nan" with None (1 or more "nan" separated by commas)
        df[column] = df[column].apply(lambda x: None if isinstance(x, str) and re.match(r'^(nan\s*,\s*)*nan$', x.strip()) else x)
    return df

# Function to clean and process the data based on the given requirements
def clean_and_process_data_v2(df):
    # Replace the exact match of 'nan, nan, nan, nan, nan, nan' with None
    df = df.applymap(lambda x: None if x == "nan, nan, nan, nan, nan, nan" else x)

    # Replace None with empty string
    df = df.applymap(lambda x: "" if x is None else x)

    # Function to process each column
    def process_column_v2(series):
        # Drop empty values ("" or equivalent)
        cleaned_values = series[~series.isin(["", None])].dropna()
        
        # Split by "~iamDiscreminator~", remove duplicates, and join with commas
        unique_items = ",".join(set(cleaned_values))
        return unique_items

    # Apply the process_column_v2 function to each column (excluding 'IssueId' as it is the key)
    cleaned_data = df.groupby('IssueId', as_index=False).agg(process_column_v2)
    
    return cleaned_data

# Step 1: Replace values like "nan, nan, nan, ..." with None
data = replace_nan_values_with_none(data)

# Clean the data with the new rules
cleaned_data_v2 = clean_and_process_data_v2(data)

# Save the cleaned data to a new Excel file
output_file_path = 'data/GPT/cleaned_combined.xlsx'  # Replace with desired output path
cleaned_data_v2.to_excel(output_file_path, index=False)

# Output the cleaned data
print("Data has been cleaned and saved to:", output_file_path)
