from abc import abstractmethod, ABCMeta
from copy import copy


class CommonDisplay(metaclass=ABCMeta):
    @abstractmethod
    def show_all(self):
        pass

    @abstractmethod
    def search(self):
        pass

    @abstractmethod
    def help(self):
        pass


class NotebookDisplay(CommonDisplay):
    def show_all(self, notebook):
        print(f">>> This is your notebook:\n")
        self.sort_by_alphabet(notebook)

    def display(self, result_notes):
        print("------------------------------------")
        for val in result_notes.data.values():
            print(f"Title: {val.note[0].title}")
            print(f"Body: {val.note[1].body}")
            print(f"Tags: {val.note[2].tag}")
            print("------------------------------------")

    def sort_by_alphabet(self, notes):
        from notebook_core import Notebook

        title_list = []
        sorted_notes = Notebook()
        for i in notes.data.keys():
            title_list.append(copy(i))
        title_list.sort()
        for val in title_list:
            sorted_notes.data[val] = notes.data[val]
        self.display(sorted_notes)

    def help(self):
        print(
            """
        You can type one of the following commands: \n
        add [new title] - to add a new note 
        search [title] - to find one of your notes
        show - to see all current notes
        edit [title] - to change a note content
        find [title] - to find notes by tags
        delete [title] - to erase a note 
        help - to see the list of commands
        exit - to end session
        """
        )

    def search(self, user_input, default_notebook):
        from notebook_core import Notebook

        title = user_input.removeprefix("search").strip()
        unfor_result = ">>> Note not found! Try again!"
        result_notes = Notebook()

        for key in default_notebook.data.keys():
            if title.capitalize() == key:
                result_notes.data[key] = default_notebook.data[key]
        if result_notes.data:
            self.display(result_notes)
        else:
            print(unfor_result)


class AddressBookDisplay(CommonDisplay):
    def show_all(self, PHONE_VOCABULAR):
        if PHONE_VOCABULAR:

            return PHONE_VOCABULAR.next()
        return f"Phone Vocabulary don`t have contact now"

    def help(self):
        return """
        Hello,here you can:
        Add to your phone vocabular contact - add + name + numer + birthday
        Change this contact - change + name + numer + new numer
        Show your contacts - phone + name
        Search your contact - search + name(first 3 letters)
        Show your all list with contacts - show
        delete contact - delete + name
        Shows how many days are left until this user's birthday - birthday + name
        And close this vocabular - exit
        """

    def search(self, sub, PHONE_VOCABULAR):
        if len(sub) < 3:
            print("Search works with 3 symbols min")
        else:
            for rec in PHONE_VOCABULAR.data.values():
                phone_row = ",".join([str(ph) for ph in rec.phones])
                if sub.lower() in rec.name.value.lower() or sub in phone_row:
                    return rec
