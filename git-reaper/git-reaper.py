import re
import subprocess
import argparse
from time import sleep


def get_branch_by_regex(pattern: str):
    matches = []
    pattern = rf"{pattern}"
    print(f"\nMake sure your pattern in correct at https://regex101.com/ using Python!")

    # Get a list of all remote branches
    all_branches = subprocess.run(
        ["git", "branch", "-r"], capture_output=True, text=True).stdout.splitlines()

    # Iterate through the branches and get a list of branches that match the pattern
    for branch in all_branches:
        if re.search(pattern, branch):
            branch = branch.replace("origin/", "").strip()
            matches.append(branch)

    return matches


def get_branch_by_age(years: int):
    matches = []

    # Get a list of remote branches with name and age
    all_branches = subprocess.run(["git", "for-each-ref", "--sort=-committerdate:iso8601",
                                   "--format=%(committerdate:relative)|%(refname:short)",
                                   "refs/remotes/"], capture_output=True, text=True)
    all_branches = str(all_branches.stdout).split('\n')

    # Iterate through the branches and append the ones that match the age or older (up to 9 years old)
    while 1 <= years <= 9:
        for branch in all_branches:
            if f"{years} year" in branch:
                branch_name = branch.split("|")[1].replace("origin/", "")
                matches.append(branch_name)
        years += 1

    return matches


def get_branch_by_age_and_pattern(years: int, pattern: str):
    matches = []

    all_branches = subprocess.run(["git", "for-each-ref", "--sort=-committerdate:iso8601",
                                   "--format='%(committerdate:relative)|%(refname:short)|%(committername)'",
                                   "refs/remotes/"], capture_output=True, text=True)
    all_branches = str(all_branches.stdout).split('\n')

    # Iterate through the branches and append the ones that match the age or older (up to 9 years old)
    while 1 <= years <= 9:
        for branch in all_branches:
            if f"{years} year" in branch:
                branch_name = branch.split("|")[1]
                branch_name = branch_name.replace("origin/", "")
                if re.search(pattern, branch_name):
                    matches.append(branch_name)
        years += 1

    return matches


deleted = 0
filtered_branches = []
# Enter the name/s of your main branch so you don't delete it by mistake
excluded_branches = ["master", "develop", "main",
                     "HEAD -> master", "HEAD -> develop", "HEAD -> main"]

print("\nScanning the repository...\n")

# Get argumens from CLI
parser = argparse.ArgumentParser()
parser.add_argument("--pattern", dest="pattern", type=str)
parser.add_argument("--age", dest="age", type=int)
args = parser.parse_args()

# Get the final list of branches based on what arguments were used
if args.age and args.pattern:
    filtered_branches = get_branch_by_age_and_pattern(args.age, args.pattern)

elif args.age:
    filtered_branches = get_branch_by_age(args.age)

elif args.pattern:
    filtered_branches = get_branch_by_regex(args.pattern)

# sanity check for the master branch (or whatever the convention is)
for excluded_br in excluded_branches:
    if excluded_br in filtered_branches:
        filtered_branches.remove(excluded_br)

if filtered_branches:
    print(f"Number of branches found: {len(filtered_branches)}\n")
    for branch in filtered_branches:
        print(branch)

    # Ask explicitly before deleting
    confirm_delete = input("\nAre you sure you want to archive and delete? [y/n]: ")

    if confirm_delete.lower()[0] == "y":
        for br in filtered_branches:
            # Archive the branch
            subprocess.run(['git', 'tag', 'archive/{}'.format(br), 'origin/{}'.format(br)], capture_output=True)
            print(f"Tagged as archive/{br}")
            # Delete the branch from remote origin
            subprocess.run(['git', 'push', 'origin', '--delete', br], capture_output=True)
            # Delete the branch from local
            # subprocess.run(['git', 'branch', '-d', br], capture_output=True)
            print(f"{br} has been deleted from origin.")
            deleted += 1
        subprocess.run(['git', 'push', '--tags'], capture_output=True)
else:
    print("\nNo matches found.")

print(f"\nExecution finished. Branches deleted: {deleted}")
