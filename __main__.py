try:
    try:
        from rich import print as cprint
        from sys import stdout
        import os
        import pickle
        import platform
        import datetime
        import inquirer
        from datetime import datetime
        import getch
    except ModuleNotFoundError as e:
        print("Could not use",e,"please add to pip")
        exit()
    try:
        os.mkdir(f"{os.environ['USERPROFILE']}/chatter")
    except FileExistsError:
        pass

    write = stdout.write
    class CmdError(Exception):
        """When the command is not valid."""
        
        def __init__(self, cmd) -> None:
            super().__init__(f'Invalid Command "{cmd}"\n"{cmd}" is not a vaild command try help.')
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
    def choose(item_name:str,message:str,items:list)->str:

        questions = [
            inquirer.List(
                item_name,
                message=message,
                choices=items,
            ),
        ]
        username = inquirer.prompt(questions)
        return username[item_name] 
    def date_maker()->str:
        forms = ["DD","MM","YY","YYYY"]
        messsage = []
        for i in range(3):
            date1 = choose("date1","What do you want first: ",forms)
            messsage
            if date1 in ("YY","YYYY"):
                del forms[forms.index("YY")]
                del forms[forms.index("YYYY")]
                messsage.append(date1)
            else:
                del forms[forms.index(date1)]
                messsage.append(date1)
            up(len(forms)+2)
            
        date_list = []
        for part in messsage:
            if part == "DD":
                date_list.append("%d")
            elif part == "MM":
                date_list.append("%m")
            elif part == "YY":
                date_list.append("%y")
            elif part == "YYYY":
                date_list.append("%Y")
        return input("Chose the seperator: ").join(date_list)
        
    def make_cmd(cmds)->list[str]:
        made_cmds = []
        cur = ""
        cont_times = 0
        is_str = False
        for cmd in cmds:
            if cont_times > 0:
                cont_times -= 1
                continue
            if cmd in ('"',"'"):
                if is_str:
                    made_cmds.append(cur)
                    cur = ""
                is_str=not is_str
                continue
            if is_str:
                cur+=cmd
                continue
            if cmd in " \t":
                made_cmds.append(cur)
                cur = ""
            cur += cmd
        if is_str:
            raise CmdError(cmds)
        return [cur] if made_cmds == [] else made_cmds

    pass_attempts = 0
    cmd_helps = {
        '"time"':"prints the time",
        '"date"':"prints the date",
        '"python"':"runs the python interprter",
        '"echo"':"prints what you put",
        '"exit"':"stops the program"
    }
    time_form = "%I:%M %P"
    date_form = "%m/%d/%y"

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
        cmd = make_cmd(input("$>"))
        print(cmd)
        if cmd[0] == "help":
            for x,y in zip(cmd_helps.keys(),cmd_helps.values()):
                print(x,y)
        elif cmd[0] == "exit":
            break
        elif cmd[0] == "echo":
            print(cmd[5:])
        elif cmd[0] == "time":
            print(date.strftime(time_form))
        elif cmd[0] == "strftime":
            print(date.strftime(cmd[2:]))
        elif cmd[0] == "date":
            print(date.strftime(date_form))
        elif cmd[0] == "settime":
            messsage = choose("Times","What format do you want to see the time?",
                            ["12:59 pm","24:59","12:59 59 pm"])
            if messsage == "12:59 pm":
                time_form = "%I:%M %P"
            elif messsage == "24:59":
                time_form = "%H:%M"
            elif messsage == "12:59 59 pm":
                time_form = "%I:%M %S %p"
        elif cmd == "setdate":
            messsage = choose("Dates","What format do you want to see the date?",
                            ["12/31/09","","12:59 59 pm"])
            if messsage == "12:59 pm":
                time_form = "%I:%M %p"
            elif messsage == "24:59":
                time_form = "%H:%M"
            elif messsage == "12:59 59 pm":
                time_form = "%I:%M %S %p"
        else:
            cprint(f"[#B00020]Error: {cmd} is not a valid command please use help for help[#B00020]",file=sys.stderr)
            
except KeyboardInterrupt:
    quit()