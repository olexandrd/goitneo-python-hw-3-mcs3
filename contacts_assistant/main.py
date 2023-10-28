from modules.assistant_classes import *
from modules.bot_commands import Commands, parse_input
from modules.persistance import AddressBookFile

ADDRESS_BOOK_FILE = "address_book.dat"


def main():
    addressBookFile = AddressBookFile(ADDRESS_BOOK_FILE)
    contacts = AddressBook(addressBookFile.load(ADDRESS_BOOK_FILE))
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)
        command_helper = Commands(args, contacts)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(command_helper.add_contact(args, contacts))
            addressBookFile.save(ADDRESS_BOOK_FILE, contacts)
        elif command == "change":
            print(command_helper.change_contact(args, contacts))
            addressBookFile.save(ADDRESS_BOOK_FILE, contacts)
        elif command == "phone":
            print(command_helper.show_phone(args, contacts))
        elif command == "all":
            print(command_helper.show_all(contacts))
        elif command == "add-birthday":
            print(command_helper.add_birthday(args, contacts))
            addressBookFile.save(ADDRESS_BOOK_FILE, contacts)
        elif command == "show-birthday":
            print(command_helper.show_birthday(args, contacts))
        elif command == "birthdays":
            print(command_helper.birthdays(contacts))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
