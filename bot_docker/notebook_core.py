from collections import UserDict
from display import NotebookDisplay
from copy import copy
import json
from os.path import isfile


file_name = "Notebook.json"
path = "./Notebook.json"
disp = NotebookDisplay()


class Title:
    def __init__(self):
        self.__title = None

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, new_value):
        if len(new_value) <= 50:
            self.__title = new_value.capitalize()
        else:
            print(">>> Your title is longer than 50 symbols. Please, make it shorter!")


class Body:
    def __init__(self):
        self.__body = None

    @property
    def body(self):
        return self.__body

    @body.setter
    def body(self, new_value):
        if len(new_value) <= 300:
            self.__body = new_value
        else:
            print(">>> Your note is longer than 300 symbols. Please, make it shorter!")


class Tag:
    def __init__(self) -> None:
        self.__tag = None

    @property
    def tag(self):
        return self.__tag

    @tag.setter
    def tag(self, value: str):
        if value:
            tag_list = value.split(" ")
            self.__tag = tag_list
        else:
            self.__tag = []


class Note:
    def __init__(self):
        self.__note = None

    @property
    def note(self):
        return self.__note

    @note.setter
    def note(self, new_list):
        self.__note = new_list


class Notebook(UserDict):

    # key: Title, value: Body -> change to Note later on
    def add(self, note):
        self.data[note.note[0].title] = note


def input_error(func):
    def inner(*args):

        try:
            func(*args)
        except IndexError:
            print("Index Error! Please try again!")
            func(*args)
        except KeyError:
            print("Key Error! Please try again!")
            func(*args)
        except ValueError:
            print("Value Error! Please try again!")
            func(*args)

    return inner


@input_error
def add_note(user_input):

    title = user_input.removeprefix("add").strip().capitalize()
    new_title = Title()
    new_body = Body()
    new_tag = Tag()
    new_note = Note()

    body_input = input(f"Enter content for new note '{title}' >>> ")
    tag_input = input(
        f"Enter tags for new note '{title}' or click 'Enter' to continue without tags >>> "
    )

    new_title.title = title
    new_body.body = body_input
    new_tag.tag = tag_input
    if new_title.title and new_body.body:
        new_note.note = [new_title, new_body, new_tag]
        default_notebook.add(new_note)
    else:
        print("Something was wrong with title or body")
        print("Try again")


@input_error
def search_note(user_input):
    disp.search(user_input, default_notebook)


@input_error
def show_all(user_input):
    disp.show_all(default_notebook)


def find_by_tag(*args):
    tags = args[0].split(" ")
    tags_list = tags[1:]
    result_tags = Notebook()
    buff_note = Note()
    for i in tags_list:
        for val in default_notebook.data.values():
            if val.note[2].tag:
                if i in val.note[2].tag:
                    buff_note.note = val.note
                    result_tags.add(copy(buff_note))
    if result_tags.data:
        disp.sort_by_alphabet(result_tags)
    else:
        print("Such tags doesn`t found")


def save(notebook):
    result = {}
    with open(file_name, "w") as fh:
        for key, val in notebook.data.items():
            notes_list = []
            note = {}
            note["Title"] = val.note[0].title
            note["Body"] = val.note[1].body
            if val.note[2].tag:
                note["Tags"] = val.note[2].tag
            notes_list.append(note)
            result[key] = notes_list
        json.dump(result, fh, indent=4)


def restore():
    global default_notebook
    with open(file_name, "r") as fh:
        unpacked = json.load(fh)
        for val in unpacked.values():
            tags = Tag()
            title = Title()
            body = Body()
            note = Note()
            title.title = val[0]["Title"]
            body.body = val[0]["Body"]
            if "Tags" in val[0].keys():
                tags.tag = " ".join(val[0]["Tags"])
            else:
                tags.tag = []
            note.note = [title, body, tags]
            default_notebook.data[title.title] = copy(note)


@input_error
def edit_note(user_input):

    new_note = Body()
    title = user_input.removeprefix("edit").strip().capitalize()

    if title not in default_notebook.data.keys():
        print(">>> Note with this name does not exist! Try again!")
    else:
        new_value = input(f"Enter new content for '{title}'>>> ")
        new_note.body = new_value
        default_notebook.data[title].note[1] = new_note
        print(">>> Note edited!")


@input_error
def delete_note(user_input):

    title = user_input.removeprefix("delete").strip().capitalize()

    if title not in default_notebook.data.keys():
        print(">>> Note with this name does not exist! Try again!")
    else:
        default_notebook.data.pop(title)
        print(">>> Note deleted!")


@input_error
def help(user_input):
    disp.help()


@input_error
def exit_helper():

    print(">>> Good bye!")


COMMANDS = {
    "add": add_note,
    "search": search_note,
    "show": show_all,
    "edit": edit_note,
    "delete": delete_note,
    "find": find_by_tag,
    "help": help,
    "exit": exit_helper,
}


def handler(command_name):
    return COMMANDS[command_name]


def main_notebook():

    print(
        """
        You are in your notebook. Enter one of the following commands: \n
        add [new title]
        search [title]
        show
        edit [title]
        find [title]
        delete [title]
        help
        exit 
        """
    )
    if isfile(path):
        restore()
    while True:
        user_input = input(">>> ")
        input_parsed = user_input.split()
        command = input_parsed[0].lower()

        if command not in COMMANDS.keys():
            print("Please enter one of the commands from the list!")
        elif command == "exit":
            exit_helper()
            break
        else:
            handler(command)(user_input)
    save(default_notebook)


default_notebook = Notebook()


if __name__ == "__main__":
    main_notebook()
