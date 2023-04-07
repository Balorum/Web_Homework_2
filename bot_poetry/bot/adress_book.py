import csv
from collections import UserDict
from datetime import datetime, timedelta
from os.path import isfile
from display import *
import os
import sys

sys.path.append(os.path.abspath("../bot_helper"))

path = "./book.csv"
display_phone = AddressBookDisplay()


class Field:  # батько для Name, Phone
    def __init__(self, value):
        self.value = value
        self.__value = None

    def __repr__(self) -> str:
        return self.value


class Name(Field):
    pass


class Phone(Field):
    """Перевірка робиться в сеттері, тобто ми створимо захищене поле
    self.__value і якщо перевірка пройде ми наше значення що прийшло запишемо в
    захищенне поле"""

    @property  # це геттер - він повертає захищенне поле
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if (
            len(value) == 10 and value.isdigit()
        ):  # тут перевірка телефона на довжину та щоб він був лише цифри
            self.__value = value

        else:
            raise ValueError(f"Wrong number - number should have 10 symbols")


class Birthday(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        try:
            bday = datetime.strptime(value, "%d.%m.%Y")
            self.__value = value
        except TypeError:
            return f"Format your birthday is not correct"


class Record:
    def __init__(self, name: Name, phone: Phone = None, birthday: Birthday = None):
        self.name = name
        self.phones = []
        if phone:
            self.phones.append(phone)
        if (
            birthday
        ):  # тут логіка яка, якщо прийшоов День Народження - то записуємо, якщо немає - то пуста строка
            self.birthday = birthday
        else:
            self.birthday = ""

    def add_phone(self, phone: Phone) -> None:
        self.phones.append(phone)

    def del_phone(self, phone: Phone) -> None:
        self.phones.remove(phone)

    def edit_phone(self, old_phone: Phone, new_phone: Phone) -> str:
        for phone in self.phones:
            if phone.value == old_phone.value:
                self.phones.remove(phone)
                self.phones.append(new_phone)
                return f"Phone for contact {self.name.value} change successful"
        return f"Contact {self.name.value} don't have phone {old_phone.value}"

    def days_to_birthday(self):
        new_date = datetime.strptime(self.birthday.value, "%d.%m.%Y")
        birthday_date = datetime.strftime(new_date, "%d.%m.%Y")
        current_date = datetime.now()
        birthday_date = birthday_date.replace(
            birthday_date[-4:], str(current_date.year)
        )
        new_birthday_date = datetime.strptime(birthday_date, "%d.%m.%Y")
        delta_days = new_birthday_date - current_date

        target_bday = datetime.strftime(new_birthday_date, "%d-%B-%Y")

        if delta_days.days > 0:
            return f"{delta_days.days} days left before {target_bday}"
        else:
            birthday_date = birthday_date.replace(
                birthday_date[-4:], str(current_date.year + 1)
            )
            new_birthday_date = datetime.strptime(birthday_date, "%d.%m.%Y")
            delta_days = new_birthday_date - current_date
            target_bday = datetime.strftime(new_birthday_date, "%d-%B-%Y")
            return f"{delta_days.days} days left before {target_bday}"

    def __repr__(self) -> str:
        return f'User {self.name} - Phones: {", ".join([phone.value for phone in self.phones])} Birthday: {self.birthday}'


class AddressBook(UserDict):
    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record

    def iterator(self, n=2):
        self.n = n  # це кількість записів на сторінці
        index = 1
        print_block = "-" * 50 + "\n"  # це типу строка для розділу сторінок
        for record in self.data.values():  # ітерується по записам record
            print_block += str(record) + "\n"
            if index < n:
                index += 1

            else:
                yield print_block
                index, print_block = 1, "-" * 50 + "\n"
        yield print_block  # тут повертається все що залишилось

    def next(self, n=2):
        result = "List of all users:\n"
        # це наш ітератор(генератор більше тому що yield)
        print_list = self.iterator(n)
        for item in print_list:  # на кожній ітерації наш ітератор повертає по 2 записи
            result += f"{item}"  # ми іх збираємо в змінну і повертаємо
        return result

    def write_book(self):
        with open("book.csv", "w", newline="") as file:
            field_names = ["name", "phones", "birthday"]
            writer = csv.DictWriter(file, fieldnames=field_names)
            writer.writeheader()
            for rec in self.data.values():
                phone_row = ",".join([str(ph) for ph in rec.phones])
                writer.writerow(
                    {
                        "name": rec.name.value,
                        "phones": phone_row,
                        "birthday": rec.birthday,
                    }
                )

    def read_book(self):
        with open("book.csv", "r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                name = Name(row["name"])
                phone_row = row["phones"]
                birthday = row["birthday"]
                if birthday:
                    obj_birthday = Birthday(birthday)
                else:
                    obj_birthday = None
                if phone_row:
                    phone_list = phone_row.split(",")
                    if len(phone_list) == 1:
                        obj_phone = Phone(phone_list[0])
                        obj_rec = Record(name, obj_phone, obj_birthday)
                    else:
                        obj_phone = Phone(phone_list[0])
                        obj_rec = Record(name, obj_phone, obj_birthday)
                        for i in phone_list[1:]:
                            obj_rec.add_phone(i)
                else:
                    obj_rec = Record(name, obj_birthday)
                self.add_record(obj_rec)


"""Функції для роботи консольного бота"""


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Give me name and phone please"
        except ValueError:
            return "Incorrect number"
        except IndexError:
            return "please input birthday date"
        except TypeError:
            return "typeerror"

    return wrapper


@input_error
def add_contact(*args: str, PHONE_VOCABULAR):
    name = Name(args[0])
    phone = Phone(args[1])
    birthday = Birthday(args[2])
    rec = Record(name, phone, birthday)
    PHONE_VOCABULAR.add_record(rec)
    return f"Contact {name.value} with phone: {phone.value} and birthday {birthday.value} was created!"


@input_error
def simple_func(args: str):
    return args.upper()


def greeting(*args):
    return "How can I help you?"


# @input_error
def show_all_phone(PHONE_VOCABULAR, *args):
    display_phone.show_all(PHONE_VOCABULAR)


def exiting(PHONE_VOCABULAR):
    PHONE_VOCABULAR.write_book()
    print("Goodbye")


def unknown(*args):
    return "Command not exist"


@input_error
def change(*args, PHONE_VOCABULAR):
    rec = PHONE_VOCABULAR.get(args[0])
    if rec:
        old_phone = Phone(args[1])
        new_phone = Phone(args[2])
        return rec.edit_phone(old_phone, new_phone)
    return f"Contact with name {args[0]} not in AddressBook"


# @input_error
# def show_phone(*args, PHONE_VOCABULAR):
#     display_phone(*args, PHONE_VOCABULAR)


@input_error
def search(*args, PHONE_VOCABULAR):
    return display_phone.search(args[0], PHONE_VOCABULAR)


def birthday(*args, PHONE_VOCABULAR):
    return PHONE_VOCABULAR.data[args[0]].days_to_birthday()


def book_helper(PHONE_VOCABULAR):
    return display_phone.help()


COMMANDS = {
    greeting: ["hello", "hi"],
    add_contact: ["add", "+"],  # add + name + numer
    exiting: ["exit", "close", "."],
    change: ["change", "edit"],  # change + name + numer + new numer
    show_all_phone: ["phone"],  # phone + name
    display_phone.show_all: ["show", "all"],
    search: ["search"],
    birthday: ["birthday"],
    book_helper: ["help"],
}


def command_parser(user_input: str):
    for command, key_words in COMMANDS.items():
        for key_word in key_words:
            if user_input.startswith(key_word):
                return command, user_input.replace(key_word, "").split()
    return unknown, None


def main_address_book():
    PHONE_VOCABULAR = AddressBook()  # створюємо обьект классу при виклику функції
    print(book_helper(PHONE_VOCABULAR=PHONE_VOCABULAR))
    if isfile(path):
        PHONE_VOCABULAR.read_book()
    while True:
        user_input = input(">>> ")

        if user_input in COMMANDS[exiting]:
            exiting(PHONE_VOCABULAR)
            break
        command, data = command_parser(user_input)
        if data:
            print(command(*data, PHONE_VOCABULAR=PHONE_VOCABULAR))
        else:
            print(command(PHONE_VOCABULAR))

    PHONE_VOCABULAR.write_book()


if __name__ == "__main__":
    """Командний бот"""

    main_address_book()
