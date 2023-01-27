### git-reaper.py  
Clean up branches based on age of last commit or Python regex pattern.  
Must be run interactively and choose options manually.  
!! Must have Python3.6 or later !! May need to use python3 {command} on older systems.  

#### Usage:
clone the repo an cd into it then run:  
python /path/to/script.py --age 2 to find and list all branches were the last commit was made 2 or more years ago  
or  
python /path/to/script.py --pattern "deploy-cc-55[0-9]+" to list all branches whose name matches the regex  
You can combine --age and --pattern to filter only results that match both conditions.  

Afterwards you will be asked if you want to archive the branch and then if you want to delete it from the server.  

### git-reaper-auto.py  
Same as above script however you pass all the parameters in the initial stage and then it runs automatically.  
There are 2 additional parameters you can use --archive and --delete  

#### Usage:  
Scenario 1 - I want to archive and delete all branches older that 2 years that contain "deploy-cc" in the name:  
clone https://git.repo/test-repo.git
cd test-repo
python path/to/git-reaper-auto.py --age 2 pattern "deploy-cc-" --archive --delete

Scenario 2 - I want to delete (without archiving) all branches that have not had a commit in 4 years or more:  
clone https://git.repo/test-repo.git
cd test-repo
python path/to/git-reaper-auto.py --age 4 --delete