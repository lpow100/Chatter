from sys import stdout
import os
import pickle
import platform
os.mkdir(f"{os.environ['USERPROFILE']}/chatter")

write = stdout.write
def up(amount):
    write(f"\u001b[{amount}A")
def right(amount):
    write(f"\u001b[{amount}C")
def down(amount):
    up(-amount)
def left(amount):
    right(-amount)
def save(data, filename):
    with open(filename,"wb") as file:
        pickle.dump(data,file)
def load(filename):
    with open(filename,"rb") as file:
        return pickle.load(file)
def clear():
    if "Windows" in platform.platform():
        os.system("cls")
    else:
        os.system("clear")

pass_attempts = 0
cmd_helps = {
    "time":"prints the time",
    "date":"prints the date",
    "python":"runs the python interprter",
    "echo":"prints what you put"
}

print("Hi I am chatter your chatbot!")
try:
    names = load(f"{os.environ['USERPROFILE']}/chatter/names.pk")
except FileNotFoundError:
    names = {}
    
print("Please enter your username")
username = input(">").lower()
if username in names.keys():
    print(f"Welcome {username}")
    while True:
        if pass_attempts == 3:
            print("You entered the wrong password too many times")
            exit()
        print("Please enter your password")
        password_attempt = input(">").lower()
        if password_attempt == names[username]:
            break
        print("Wrong password please try again")
        pass_attempts += 1
else:
    while True:
        clear()
        print("Enter your password")
        password_attempt1 = input(">")
        print("Confirm your password")
        password_attempt2 = input(">")
        if password_attempt1 == password_attempt2:
            print("New user added")
            names[username] = password_attempt1
            break
    
save(names,f"{os.environ['USERPROFILE']}/chatter/names.pk")
while True:
    cmd = input("$> ")
    if cmd == "help":
        for x,y in zip(cmd_helps.keys(),cmd_helps.values()):
            print(x,y)