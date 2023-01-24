import re
import subprocess
import argparse
from time import sleep


def delete_remote_branches_by_regex(pattern: str):
    global deleted
    pattern = rf"{pattern}"
    matches = []
    print(f"\nMake sure your pattern in correct at https://regex101.com/ using Python!")

    # Get a list of all remote branches
    all_branches = subprocess.run(
        ["git", "branch", "-r"], capture_output=True, text=True).stdout.splitlines()

    # Iterate through the branches and get a list of branches that match the pattern
    for branch in all_branches:
        if re.search(pattern, branch):
            branch = branch.replace("origin/", "").strip()
            matches.append(branch)

    # Terminate the scrip if there are no matches
    if len(matches) == 0:
        print("No matches found.")
        return False

    # a simple keep-your-job check 
    # you may have different naming convention than us so change accordingly
    if "HEAD -> develop" in matches:
        matches.remove("HEAD -> develop")
    if "develop" in matches:    
        matches.remove("develop")

    print(f"Number of branches found: {len(matches)}\n")
    for match in matches:
        print(match)

    confirm_delete = input("\nAre you sure you want to delete? [y/n]: ")

    # Ask explicitly before deleting
    if confirm_delete.lower()[0] == "y":
        for br in matches:
            #subprocess.run(['git', 'push', 'origin', '--delete', br], capture_output=True)
            print(f"{br} has been deleted")
            deleted += 1
    sleep(1)


def delete_remote_branches_by_age(years: int):
    global deleted
    matches = []

    # Get a list of remote branches with age and last committer
    all_branches = subprocess.run(["git", "for-each-ref", "--sort=-committerdate:iso8601",
                                   "--format='%(committerdate:relative)|%(refname:short)|%(committername)'",
                                   "refs/remotes/"], capture_output=True, text=True)
    all_branches = str(all_branches.stdout).split('\n')

    # Iterate through the branches and append the ones that match the age or older (up to 9 years old)
    while 1 <= years <= 9:
        for branch in all_branches:
            if f"{years} year" in branch:
                tokens = branch.split("|")
                age = tokens[0][1:]
                branch_name = tokens[1]
                branch_name = branch_name.replace("origin/", "")
                commiter = tokens[2][:-1]

                matches.append([age, branch_name, commiter])
        years += 1

    # Terminate the scrip if there are no matches
    if len(matches) == 0:
        print("No matches found.")
        return False

    # a simple keep-your-job check
    if "HEAD -> develop" in matches:
        matches.remove("HEAD -> develop")
    if "develop" in matches:    
        matches.remove("develop")

    print(f"Number of branches found: {len(matches)}\n")

    for match in matches:
        print(f"{match[1]}, commited by {match[2]}, {match[0]}")

    # Ask explicitly before deleting
    confirm_delete = input("\nAre you sure you want to delete? [y/n]: ")

    if confirm_delete.lower()[0] == "y":
        for br in matches:
            #subprocess.run(['git', 'push', 'origin', '--delete', br[1]], capture_output=True)
            print(f"{br[1]} has been deleted")
            deleted += 1
    sleep(1)


def delete_by_age_and_pattern(years: int, pattern: str):
    global deleted
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

    # Terminate the scrip if there are no matches
    if len(matches) == 0:
        print("No matches found.")
        return False

    # a simple keep-your-job check 
    # you may have different naming convention than us so change accordingly
    if "HEAD -> develop" in matches:
        matches.remove("HEAD -> develop")
    if "develop" in matches:    
        matches.remove("develop")

    print(f"Number of branches found: {len(matches)}\n")
    for match in matches:
        print(match)

    confirm_delete = input("\nAre you sure you want to delete? [y/n]: ")

    # Ask explicitly before deleting
    if confirm_delete.lower()[0] == "y":
        for br in matches:
            #subprocess.run(['git', 'push', 'origin', '--delete', br], capture_output=True)
            print(f"{br} has been deleted")
            deleted += 1


deleted = 0

print("Scanning the repository...\n")

# Get argumens from CLI
parser = argparse.ArgumentParser()
parser.add_argument("--pattern", dest="pattern", type=str)
parser.add_argument("--age", dest="age", type=int)
args = parser.parse_args()

if args.age and args.pattern:
    delete_by_age_and_pattern(args.age, args.pattern)

elif args.age:
    delete_remote_branches_by_age(args.age)

elif args.pattern:
    delete_remote_branches_by_regex(args.pattern)

print(f"\nExecution finished. Branches deleted: {deleted}")
