try:
    from rich import print
    from sys import stdout
    import os
    import pickle
    import platform
    import datetime
    import inquirer
    from datetime import datetime
except ModuleNotFoundError as e:
    print("Could not use",e,"please add to pip")
    exit()
try:
    os.mkdir(f"{os.environ['USERPROFILE']}/chatter")
except FileExistsError:
    pass

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
def choose(item_name:str,message:str,items:list):

    questions = [
        inquirer.List(
            item_name,
            message=message,
            choices=items,
        ),
    ]
    username = inquirer.prompt(questions)
    return username[item_name] 

pass_attempts = 0
cmd_helps = {
    "time":"prints the time",
    "date":"prints the date",
    "python":"runs the python interprter",
    "echo":"prints what you put",
    "exit":"stops the program"
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
        password_attempt = input(">")
        password_length = len(password_attempt)
        password_length += 1
        up(1)
        print("*" * password_length)
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
    date = datetime.now()
    cmd = input("$>")
    if cmd == "help":
        for x,y in zip(cmd_helps.keys(),cmd_helps.values()):
            print(x,y)
    elif cmd == "exit":
        break
    elif cmd.startswith("echo"):
        print(cmd[5:])
    elif cmd == "time":
        print(date.strftime("[white]%X[white]"))
    elif cmd.startswith("strftime "):
        print(date.strftime(cmd[9:]))
    elif cmd == "date":
        print(date.strftime("[white]%m:%d:%Y[white]"))
    elif cmd == "settime":
        messsage = choose("Times","What format do you want to see the time?",
                          ["12:59 pm","24:59"])
        if messsage == "12:59 pm":
            time_form = "%I:%M %P"
        elif messsage == "24:59":
            time_form = "%H:%M"
    else:
        print(f'[red]Error:\n   "{cmd}"\nUnknown command: {cmd}[red]')