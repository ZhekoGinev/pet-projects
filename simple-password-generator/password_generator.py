from random import choice
from time import sleep
from datetime import datetime

character_table = list("0123456789" 
+ "abcdefghijklmnopqrstuvwxyz" 
+ "ABCDEFGHIJKLMNOPQRSTUVWXYZ" 
+ "~`!@#$%^&*()_-+={[}]|\:;\"'<,>.?/")

while True:
    length = ''
    while not length.isdigit():
        length = input("Select password length: ")
    length = int(length)

    password = ''
    for _ in range(length):
        password += choice(character_table)

    print(f"\nPassword generated successfully:  {password}\n")
    save = ''
    save = input("Would you like to save the password? [Y/n]: ")
    print()
    if save.lower() in ('y', 'yes'):
        with open('passwords.txt', 'a') as f:
            time = str(datetime.now())[:19]
            print(f"{time} - size({length}) -> {password}\n----------", file=f)
    
    again = ''
    again = input("Do you wish to generate another password? [Y/n]: ")
    if again.lower() in ('y', 'yes'):
        continue
    else:
        print("Program terminated")
        sleep(2)
        break
