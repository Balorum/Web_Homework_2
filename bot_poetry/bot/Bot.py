from adress_book import *
from main import *
from notebook_core import *
from colorama import init, Back, Style, Fore

init(autoreset=True)


def main():
    helper()

    while True:
        command = input(">>> ").split(" ")
        if command[0].lower() == "address":
            main_address_book()
        elif command[0].lower() == "notebook":
            main_notebook()
        elif command[0].lower() == "file":
            path_function()
        elif command[0].lower() == "help":
            helper()
        elif command[0].lower() == "exit":
            print("Good bye")
            break
        else:
            print("Such command does not exist. Try again ")
        print("Enter the command or 'help' to see commands")


def helper():
    print(
        """This bot has 3 functions:
    Address book, Notebook and File sorter
    Please Enter one of this command:"""
    )
    print(Fore.BLUE + "1) Address book")
    print(Fore.YELLOW + "2) Notebook")
    print(Fore.GREEN + "3) File sorter")
    print("or 'exit' to exit :)")


main()
