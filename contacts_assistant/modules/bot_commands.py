from modules.assistant_classes import *

def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return f"Please type: \033[1m{func.__name__.rstrip('_contact')} username phone\033[0m."
        except IndexError:
            return f"User name missing, type: \033[1mphone username\033[0m."
        except KeyError:
            return "Contact not found. Please add contact first."

    return wrapper

def parser_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Empty command."

    return wrapper

@parser_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


class Commands:
    def __init__(self, args, contacts):
        self.args = args
        self.address_book = contacts

    @input_error
    def add_contact(self, args, contacts: AddressBook) -> str:
        name, phone = args
        new_record = Record(name)
        new_record.add_phone(phone)
        contacts.add_record(new_record)
        return "Contact added."


    @input_error
    def change_contact(self, args, contacts: AddressBook) -> str:
        name, old_phone, new_phone = args
        if contacts.find(name):
            record = Record(name)
            record.edit_phone(old_phone, new_phone)
            res = "Contact changed."
        else:
            res = "Contact not found. Please add contact first."
        return res


    @input_error
    def show_phone(self, args, contacts: AddressBook) -> str:
        name = args[0]
        return contacts.find(name)



    def show_all(self, contacts: AddressBook) -> str:
        res = str()
        for items in contacts.data.values():
            res = res + f"{items},\n"
        res = res.rstrip(",\n")
        return res
    
    @input_error
    def add_birthday(self, args, contacts: AddressBook) -> str:
        name, birthday_date = args
        if contacts.find(name):
            record = Record(name)
            record.add_birthday(birthday_date)
            res = "Birthday changed."
        else:
            res = "Contact not found. Please add contact first."
        return res
    
    @input_error
    def show_birthday(self, args, contacts: AddressBook) -> str:
        name = args
        if contacts.find(name):
            res = contacts.show_birthday(name)
        else:
            res = "Contact not found. Please add contact first."
        return res    

    def birthdays(self, contacts: AddressBook) -> str:
        return contacts.get_birthdays_per_week()

