from termcolor import cprint
from sys import stdout
import os
import pickle
import platform

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
    if platform.platform() == "Windows":
        os.system("clr")
    else:
        os.system("clear")


print("Hi I am chatter your chatbot!")
try:
    names = load("names.pk")
except FileNotFoundError:
    names = {}
    
print("Please enter your username")
username = input(">").lower()
if username in names.keys():
    print(f"Welcome {username}")
    while True:
        print("Please enter your password")
        password_attempt = input(">").lower()
        if password_attempt == names[username]:
            break
        print("Wrong password please try again")
else:
    