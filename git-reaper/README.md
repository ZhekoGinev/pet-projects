### git-reaper.py  
Clean up branches based on age of last commit or Python regex pattern.  
!! Must have Python3.6 or later !! May need to use python3 {command} on older systems.  

#### Usage:
clone the repo you want to cleanup, cd into it and then run:  

python /path/to/git-reaper.py --age 2 to find and list all branches were the last commit was made 2 or more years ago  

or  

python /path/to/git-reaper.py --pattern "deploy-55[0-9]+" to list all branches whose name matches the regex  

You can combine --age and --pattern to filter only results that match both conditions.  

##### !! You must chose additional parameters in order for the operation to actually execute !! :  

- Use --interactive if you want to be specifically asked and manully confirm y/n:  
1. If you want to archive the all branches that match.  
2. If you want to delete all the branches that match.  
This option is best if you want to test how the script works or you feel more comfortable having full control over the process.
  
- Use --archive and/or --delete to respectively archive and/or delete the branches.  
This option will do everything automatically without any interaction and is best suited for automation!  
If for some unknown reason you use both --archive/delete AND --interactive the script will ignore the --interactive parameter!  

Scenario - I want to archive and then delete all branches older than 4 years that match the pattern "deploy":  
git clone https://test-repo.git
cd test-repo  

1. Interactively:  
python path/to/git-reaper.py --age 4 --pattern "deploy" --interactive  
\>>> Do you want to archive [y/n]: y  
\>>> Do you want to delete? [y/n]: y  

2. Automatically:  
python path/to/git-reaper.py --age 4 --pattern "deploy" --archive --delete
