import pandas as pd

# Function to update rows with missing 'Id' in the Analysis file using data from the distinct issues file
def update_missing_ids_with_emails_and_keywords(distinct_issues_path, analysis_path, output_path):
    # Load the distinct issues and analysis dataframes
    distinct_issues_df = pd.read_excel(distinct_issues_path)
    analysis_df = pd.read_excel(analysis_path)

    # Print the column names of both dataframes to check for discrepancies
    print("Columns in Analysis DataFrame:", analysis_df.columns)
    print("Columns in Distinct Issues DataFrame:", distinct_issues_df.columns)

    # Normalize column names (remove leading/trailing spaces and ensure proper capitalization)
    analysis_df.columns = analysis_df.columns.str.strip()  # Remove any leading/trailing spaces
    distinct_issues_df.columns = distinct_issues_df.columns.str.strip()

    # Rename columns to match 'IssueId' and other necessary fields if required
    distinct_issues_df.rename(columns={'Issue IDs': 'IssueId', 'Matched Keywords': 'Matched Keywords'}, inplace=True)

    # Merge the dataframes on 'IssueId' to get the corresponding email, tactics, and matched keywords
    merged_df = pd.merge(analysis_df, distinct_issues_df[['IssueId', 'Email ID', 'Tactic', 'Matched Keywords']], 
                         on='IssueId', how='left')
    
    # Update only rows where 'Id' is missing (NaN)
    merged_df.loc[merged_df['Id'].isna(), 'Id'] = merged_df['Email ID']
    merged_df.loc[merged_df['Id'].isna(), 'Tactics'] = merged_df['Tactic']
    merged_df.loc[merged_df['Id'].isna(), 'Matched Keywords(Quality Attributes)'] = merged_df['Matched Keywords']

    # Drop the additional columns (Email ID, Tactics, Matched Keywords) after updating
    merged_df.drop(columns=['Email ID', 'Tactic', 'Matched Keywords'], inplace=True)

    # Ensure only the original columns from the analysis dataframe are retained
    original_columns = analysis_df.columns
    final_df = merged_df[original_columns]

    # Save the updated DataFrame to a new Excel file
    final_df.to_excel(output_path, index=False)

    print(f"Updated Analysis file saved to: {output_path}")

# Paths to the input and output files
distinct_issues_path = 'data/output/distinct_issues_with_emails_and_keywords.xlsx'  # Replace with actual path
analysis_path = 'data/output/Analysis_07.12.2024.xlsx'    # Replace with actual path
output_path = 'data/output/Analysis_08.12.2024.xlsx'               # Replace with desired output file path

# Run the function to update the analysis file
update_missing_ids_with_emails_and_keywords(distinct_issues_path, analysis_path, output_path)
