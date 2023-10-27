from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        super().__init__(value)

    def __str__(self):
        return str(self.value)


class Phone(Field):
    def __init__(self, value):
        self.__number = None
        super().__init__(value)

    @property
    def value(self):
        return self.__number

    @value.setter
    def value(self, value):
        if value.isdigit() and len(value) == 10:
            self.__number = value
        else:
            raise ValueError("Phone number is invalid.")

    def __str__(self):
        return self.value


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone: str):
        self.phones.append(Phone(phone))

    def delete_phone(self, phone: str):
        for index, phonenumber in enumerate(self.phones):
            if phonenumber.value == phone:
                self.phones.pop(index)

    def edit_phone(self, old_phone: str, new_phone: str):
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone

    def find_phone(self, phone: str):
        found_phone = None
        for phonenumber in self.phones:
            if phonenumber.value == phone:
                found_phone = phonenumber
                break
        return found_phone

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, record):
        res = None
        if record in self.data:
            res = self.data[record]
        return res

    def delete(self, record):
        if record in self.data:
            self.data.pop(record)


def main():
    # Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

    # Видалення запису Jane
    book.delete("Jane")


if __name__ == "__main__":
    main()
