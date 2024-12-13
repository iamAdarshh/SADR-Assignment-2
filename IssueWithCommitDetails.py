from typing import List

class IssueWithCommitDetailsFile:
    def __init__(self, name: str, added_methods: str, removed_methods: str, 
                 modified_methods: str, content: str, content_before: str):
        self.name = name
        self.added_methods = added_methods
        self.removed_methods = removed_methods
        self.modified_methods = modified_methods
        self.content = content
        self.content_before = content_before

    def __repr__(self):
        return f"IssueWithCommitDetailsFile(name={self.name}, added_methods={self.added_methods}, " \
               f"removed_methods={self.removed_methods}, modified_methods={self.modified_methods})"


class IssueWithCommitDetails:
    def __init__(self, id: str, hash: str, message: str, date: str, files: List[IssueWithCommitDetailsFile]):
        self.id = id
        self.hash = hash
        self.message = message
        self.date = date
        self.files = files

    def __repr__(self):
        return f"IssueWithCommitDetails(id={self.id}, hash={self.hash}, message={self.message}, " \
               f"date={self.date}, files={len(self.files)} files)"
