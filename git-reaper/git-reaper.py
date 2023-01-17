import re
import subprocess


def delete_remote_branches(pattern):
    # Get a list of all remote branches
    branches = subprocess.run(['git', 'branch', '-r'], capture_output=True, text=True).stdout.splitlines()

    # Iterate through the branches and delete the ones that match the pattern
    for branch in branches:
        if re.search(pattern, branch):
            branch = branch.replace("origin/", "").strip()
            subprocess.run(['git', 'push', 'origin', '--delete', branch], capture_output=True)

# Edit the pattern to match branch name
delete_remote_branches(r"enter_pattern_here")
