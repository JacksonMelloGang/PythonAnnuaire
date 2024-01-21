import os

def clear():
    # if windows, use cls instead of clear
    if(os.name == "nt"):
        os.system("cls")
    else:
        os.system("clear")