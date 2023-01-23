import re
import subprocess
import argparse


def delete_remote_branches_by_regex(pattern):
    global deleted
    pattern = rf"{pattern}"
    matched = []
    # Get a list of all remote branches
    branches = subprocess.run(
        ['git', 'branch', '-r'], capture_output=True, text=True).stdout.splitlines()

    # Iterate through the branches and get a list of the ones that match the pattern
    for branch in branches:
        if re.search(pattern, branch):
            branch = branch.replace('origin/', '').strip()
            matched.append(branch)
            # subprocess.run(['git', 'push', 'origin', '--delete', branch], capture_output=True)

    if len(matched) == 0:
        return False

    print(f"Number of branches found: {len(matched)}\n")
    for i in matched:
        print(i)
    to_delete = input("\nAre you sure you want to delete? [y/n]: ")
    if to_delete:
        for br in matched:
            # subprocess.run(['git', 'push', 'origin', '--delete', br], capture_output=True)
            print(f"{br} deleted")
            deleted += 1


def delete_remote_branches_by_age(years):
    global deleted
    matched = []

    # Get a list of remote branches with age and committer
    result = subprocess.run(["git", "for-each-ref", "--sort=-committerdate:iso8601",
                            "--format='%(committerdate:relative)|%(refname:short)|%(committername)'",
                             "refs/remotes/"], capture_output=True, text=True)
    result = str(result.stdout).split('\n')

    # Iterate through the branches and append the ones that match the age
    for branch in result:
        if f"{years} year" in branch:
            tokens = branch.split("|")
            age = tokens[0][1:] #0
            branch_name = tokens[1] #1
            branch_name = branch_name.replace("origin/", "")
            commiter = tokens[2][:-1] #2

            matched.append([age, branch_name, commiter])

    if len(matched) == 0:
        return False

    print(f"Number of branches found: {len(matched)}\n")
    for i in matched:
        print(f"{i[1]}, commited by {i[2]}, {i[0]}")
    to_delete = input("\nAre you sure you want to delete? [y/n]: ")
    if to_delete:
        for br in matched:
            # subprocess.run(['git', 'push', 'origin', '--delete', br[1]], capture_output=True)
            print(f"{br[1]} deleted")
            deleted += 1


print("\nReaper is searching...\n")

deleted = 0

# Get argumens from CLI
parser = argparse.ArgumentParser()
parser.add_argument("--pattern", dest="pattern", type=str)
parser.add_argument("--age", dest="age", type=int)
args = parser.parse_args()

if args.age:
    delete_remote_branches_by_age(args.age)
if args.pattern:
    delete_remote_branches_by_regex(args.pattern)

print(f"\nExecution finished. Branches deleted: {deleted}")
