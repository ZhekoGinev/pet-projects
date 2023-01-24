### Script to clean up branches from a repo based on age of last commit or python regex pattern.  

### Usage:  
cd into your repo and run the script using one or both of the optional arguments  
You may want to run git pull/fetch first to get get any recent changes:  

--age 42 - when you want to delete branches where the last commit was done 42 years ago or older.  
--pattern "regex_pattern_here"  

example:  

user@host/repo/ #: python3 /path/to/git-reaper.py --age 2  
or  
user@host/repo/ #: python3 /path/to/git-reaper.py --pattern "deploy-0[0-9]+"  
or both  
user@host/repo/ #: python3 /path/to/git-reaper.py --age 2 --pattern "deploy-0[0-9]+"  

the last one will show only branches that have both the age and the pattern.  

