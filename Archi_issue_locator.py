import os
import re
import pandas as pd
from pydriller import Repository
import git

def extract_part_from_string(input_string):
    # Replace backslashes with forward slashes to standardize the path
    input_string = input_string.replace("\\", "/")
    # Extract the part of the string after the last slash
    file_name = os.path.basename(input_string)
    # Remove the file extension and return the result
    return file_name.split('.')[0]

# Function to extract the IssueId from commit message
def extract_issue_id(commit_message):
    # Define the pattern for IssueId (AXIS2-XXXX)
    pattern = r'AXIS2-\d+'
    return re.findall(pattern, commit_message)

# Function to get method changes (added, removed, and modified) in a commit using PyDriller
def get_method_changes(file_path, commit_hash, repo_dir):
    methods_added = []
    methods_removed = []
    methods_modified = []

    # Using PyDriller to mine the commit's code changes
    for commit in Repository(repo_dir, single=commit_hash).traverse_commits():
        # Get the modified file changes in the commit
        for file in commit.modified_files:
            if os.path.basename(file.filename) == os.path.basename(file_path):
                
                methods_before = set([method.name for method in file.methods_before])
                methods_after = set([method.name for method in file.methods])
                
                # Determine methods that were added, removed, and modified
                methods_added = list(methods_after - methods_before)  # Methods added
                methods_removed = list(methods_before - methods_after)  # Methods removed
                methods_modified = [method.name for method in file.changed_methods]  # Modified methods
    
    return methods_added, methods_removed, methods_modified

# Function to process each file path and find commits containing IssueIds
def process_file_paths(file_path, repo_dir):
    # Open the file containing paths
    with open(file_path, 'r') as f:
        file_paths = f.readlines()

    # Strip newlines from each path
    file_paths = [path.strip() for path in file_paths]

    # Extract the tactic name from the .txt file name (e.g., "ActiveRedundancy" from "ActiveRedundancy.txt")
    tactic_name = extract_part_from_string(file_path)

    # Open the specified Git repository
    repo = git.Repo(repo_dir)

    # List to store the results for the Excel file
    results = []

    # Iterate through each file path
    for file_path in file_paths:
        print(f"Processing file: {file_path}")

        # Get the commit history for this file
        commits = list(repo.iter_commits(paths=file_path))

        # Iterate through each commit
        for commit in commits:
            # Check for IssueId in the commit message
            issue_ids = extract_issue_id(commit.message)

            if issue_ids:
                # Get method changes for this commit using PyDriller
                methods_added, methods_removed, methods_modified = get_method_changes(file_path, commit.hexsha, repo_dir)
                
                # If an IssueId is found, process and store the details
                for issue_id in issue_ids:
                    # Prepare data for the Excel columns
                    results.append({
                        "Id": "",  # Empty, or populate as needed
                        "Title": "",  # Empty, or populate as needed
                        "ThreadId": "",  # Empty, or populate as needed
                        "Category": "",  # Empty, or populate as needed
                        "MatchedKeywords(Quality Attributes)": "",  # Empty, or populate as needed
                        "IssueId": issue_id,
                        "IssueLink": "",  # Empty, or populate as needed
                        "Justification": "",  # Empty, or populate as needed
                        "Tactics": tactic_name,  # Use the tactic name extracted from the filename
                        "Commit ID": commit.hexsha,
                        "Commit Message": commit.message,
                        "Methods Added": ", ".join(methods_added),
                        "Methods Removed": ", ".join(methods_removed),
                        "Methods Modified": ", ".join(methods_modified),
                        "How did you find it??(Emails to issue to code) or (Code to issue to email)": "code to issue to email",
                        "FileName": os.path.basename(file_path),
                    })

    # Create a DataFrame from the results
    df = pd.DataFrame(results)

    # Save the DataFrame to an Excel file
    output_file = f"data/output/commit_issue_details_{tactic_name}.xlsx"
    df.to_excel(output_file, index=False)

    print(f"Results saved to {output_file}")

# Main entry point for the script
if __name__ == '__main__':
    tactics = ["ActiveRedundancy", "Audit", "Authenticate", "LoadBalancing", "PingEcho", "Pooling", "RBAC", "Scheduler", "Session", "ValidationInterceptor"]
    # Replace with your actual .txt file path and Git repository path

    for tactic in tactics:
        print(f"Processing tactic: {tactic}")
        file_path = f'/Users/adarshchoudhary/Documents/University of Paderborn/Software Architecture Design and Recovery/Assignment 2/code/data/archi/axis\\TxtTacticFiles\\{tactic}.txt'
        repo_dir = '/Users/adarshchoudhary/Documents/University of Paderborn/Software Architecture Design and Recovery/Assignment 2/code/axis-axis2-java-core'  # Specify the path to your Git repository
        process_file_paths(file_path, repo_dir)
        print(f"Finished processing tactic: {tactic}")
        print("-------------------------------------------------")
