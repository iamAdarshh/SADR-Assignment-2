from pydriller import Repository, Commit, ModifiedFile
from typing import Optional
import os
from constants import ARCHI_OUTPUT_FILES

from IssueWithCommitDetails import IssueWithCommitDetails, IssueWithCommitDetailsFile

import re
from typing import List

def extract_issue_ids(text: str) -> Optional[str]:
    """
    Extracts all issue IDs in the format AXIS2-<number> from the provided text.

    Args:
        text (str): The string to search for the issue IDs.

    Returns:
        List[str]: A list of extracted issue IDs or an empty list if no valid issue IDs are found.
    """
    # Regular expression to match issue IDs like AXIS2-2000, AXIS2-192, etc.
    issue_ids = re.findall(r'AXIS2-\d+', text)

    if not issue_ids:
        return None
    
    return issue_ids[0]

def commit_contains_file(commit: Commit, file_path: str) -> bool:
    """
    Check if a commit contains a specific file.
    
    :param repo: git.Repo object
    :param commit: git.Commit object
    :param file_path: str, path to the file
    :return: bool, True if the file is in the commit, False otherwise
    """
    try:
        commit.modified_files / file_path
        return True
    except KeyError:
        return False

def read_commit_file(file: ModifiedFile) -> Optional[IssueWithCommitDetailsFile]:
    """
    Read the content of a file in a commit.
    
    :param file: git.ModifiedFile object
    :return: dict, content of the file
    """
    try:
        content = file.source_code
        content_before = file.source_code_before

        # Get the methods before and after the commit
        methods_before = set([method.name for method in file.methods_before])
        methods_after = set([method.name for method in file.methods])

        file_details: IssueWithCommitDetailsFile = {
            "name": file.filename,
            "added_methods": list(methods_after - methods_before),
            "removed_methods": list(methods_before - methods_after),
            "modified_methods": [method.name for method in file.changed_methods],
            "content": content,
            "content_before": content_before
        }
        return file_details
    except Exception as e:
        print(f"Error reading file {file.filename}: {e}")
        return None

def get_commit_details(commit: Commit, file_path: str, file_type: str) -> Optional[IssueWithCommitDetails]:
    if any(file.filename == file_path and file.filename.endswith(file_type) for file in commit.modified_files):

        issueId = extract_issue_ids(commit.msg)

        files: list[IssueWithCommitDetailsFile] = []

        print(commit.modified_files)
        for file in commit.modified_files:
            if file.filename == file_path and file.filename.endswith(file_type):
                file_details = read_commit_file(file)
                if file_details:
                    files.append(file_details)

        commit_details: IssueWithCommitDetails = {
            "id": issueId,
            "hash": commit.hash,
            "message": commit.msg,
            "date": commit.committer_date,
            "files": files
        }

        return commit_details
    return None

def extract_part_from_string(input_string):
    # Replace backslashes with forward slashes to standardize the path
    input_string = input_string.replace("\\", "/")
    # Extract the part of the string after the last slash
    file_name = os.path.basename(input_string)
    # Remove the file extension and return the result
    return file_name.split('.')[0]

if __name__ == "__main__":
    repo_path = "axis-axis2-java-core"

    issues:list[IssueWithCommitDetails] = []

    print()
    for file in ARCHI_OUTPUT_FILES:
        with open(file, 'r') as archi_file:
            filenames = archi_file.read().splitlines()

        for filename in filenames:
            print(f"Searching for issues in file: {filename}");
            repository = Repository(repo_path)
            for commit in repository.traverse_commits():
                if commit.modified_files:
                    print(commit.modified_files[0].filename)
                commit_details = get_commit_details(commit, filename, ".txt")
                if commit_details:
                    issues.append(commit_details)

        print("Issues found:", len(issues))
        print()
        