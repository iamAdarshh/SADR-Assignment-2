import re
from datetime import datetime
import pandas as pd
from pydriller import Repository
import git

# Function to read IssueIds from Excel, filtering out rows where FileName already has a value
def read_and_correct_issue_ids_from_excel(excel_file):
    df = pd.read_excel(excel_file)
    
    # Filter out rows where 'FileName' has a value
    df_filtered = df[df['FileName'].isna()]
    
    # Correct the IssueIds: Capitalize and add "AXIS2-" prefix if missing
    issue_ids = df_filtered['IssueId'].dropna().tolist()
    
    corrected_issue_ids = []
    for issue_id in issue_ids:
        # Capitalize and add "AXIS2-" prefix if missing
        issue_id = issue_id.upper()
        if not issue_id.startswith("AXIS2-"):
            issue_id = "AXIS2-" + issue_id
        corrected_issue_ids.append(issue_id)
    
    return corrected_issue_ids

# Function to extract the IssueId from commit message considering delimiters like space, newline, or period
def extract_issue_id(commit_message):
    # Pattern to match IssueIds like AXIS2-1000, AXIS2-10000, etc., ending with space, newline, or period
    pattern = r'AXIS2-\d+(?=\s|\.|\n|$|,)'
    return re.findall(pattern, commit_message)


# Function to get method changes (added, removed, and modified) in a commit using PyDriller
def get_method_changes(commit_hash, repo_dir):
    file_changes = {}

    # Traverse the commits in the repository
    for commit in Repository(repo_dir, single=commit_hash).traverse_commits():
        # Iterate through the modified files in the commit
        for file in commit.modified_files:
            # Initialize the method lists for this file if not already present
            if file.filename not in file_changes:
                file_changes[file.filename] = {
                    "added": [],
                    "modified": [],
                    "removed": []
                }

            # Get the methods before and after the commit
            methods_before = set([method.name for method in file.methods_before])
            methods_after = set([method.name for method in file.methods])

            # Determine methods that were added, removed, and modified
            file_changes[file.filename]["added"] = list(methods_after - methods_before)
            file_changes[file.filename]["removed"] = list(methods_before - methods_after)
            file_changes[file.filename]["modified"] = [method.name for method in file.changed_methods]

    return file_changes

# Function to process commits and find commits related to IssueIds
def process_commits(repo_dir, issue_ids):
    results = []

    repo = git.Repo(repo_dir)

    for issue_id in issue_ids:
        # Find commits that are associated with the given IssueId
        commits = list(repo.iter_commits('master'))  # Replace 'master' with the appropriate branch if necessary

        for commit in commits:
            # Check if commit message contains the IssueId
            if issue_id in extract_issue_id(commit.message):
                files = get_method_changes(commit.hexsha, repo_dir)
                
                results.append({
                    "IssueId": issue_id,
                    "Commit ID": commit.hexsha,
                    "Commit Message": commit.message,
                    "Commit Date": datetime.fromtimestamp(commit.committed_date).isoformat(),
                    "files": files,
                    #"Methods Added": ", ".join(methods_added),
                    #"Methods Removed": ", ".join(methods_removed),
                    #"Methods Modified": ", ".join(methods_modified),
                    #"FileName": commit.filename,
                })

    return results

# Function to read IssueIds from an Excel file
def read_issue_ids_from_excel(excel_file):
    df = pd.read_excel(excel_file)
    issue_ids = df['IssueId'].dropna().tolist()
    return issue_ids

# Main function to extract and save the commit details
def main():
    # Path to the Excel file with IssueIds
    excel_file = 'data/output/Analysis_07.12.2024.xlsx'  # Replace with your actual Excel file path
    
    # Path to your Git repository
    repo_dir = 'axis-axis2-java-core'  # Replace with your actual Git repository path
    
    # Read and correct IssueIds from Excel
    issue_ids = read_and_correct_issue_ids_from_excel(excel_file)

    # Process commits related to the IssueIds
    results = process_commits(repo_dir, issue_ids)

    # Convert the results to a DataFrame
    df = pd.DataFrame(results)

    # Save the results to an Excel file
    output_file = 'data/output/missing_commits.xlsx'  # Replace with the desired output file path
    df.to_excel(output_file, index=False)

    print(f"Results saved to {output_file}")

if __name__ == '__main__':
    main()
