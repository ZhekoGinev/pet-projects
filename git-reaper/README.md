This is a repository branch cleaner that will use a regex pattern to delete all branches that match the pattern.

Example Usage (linux syntax):  
***git clone https://github.com/ZhekoGinev/pet-projects.git  
cd pet-projects/git-reaper***

***nano git-reaper.py***  
Change "enter_pattern_here" on line 16 to the regex/string you wish to match in the branch name to be deleted.
***delete_remote_branches(r"test/.\*")***  
ctrl+s to save, ctrl+x to exit nano  

Run the script: ***python git-reaper.py***  

This will delete all branches in the current git repo (in our example zhekoginev/pet-projects that start with "test/"
