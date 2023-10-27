import re
from collections import UserDict, defaultdict
from datetime import datetime, timedelta


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

class Birthday(Field):
    def __init__(self, value):
        self.__birthday = None
        super().__init__(value)
        super()


    @property
    def value(self):
        return self.__birthday

    @value.setter
    def value(self, value):
        date_format = "%d.%m.%Y"
        try:
            self.__birthday = datetime.strptime(value, date_format)
        except:
            raise ValueError("Date format is invalid. It should be DD.MM.YYYY")


    def __repr__(self):
        return self.value
    
    def __str__(self):
        return str(self.value)
    


class BirthdaysPerWeek:
    def __init__(self, contacts):
        self.contacts = contacts    

    @classmethod
    def weekday_to_number(self, weekday):
        weekdays = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]
        return weekdays.index(weekday)
    
    def get_birthdays_per_week(self, contacts) -> defaultdict:
        today = datetime.today()
        res = defaultdict(list)
        for d in contacts.values():
            # Check if birthday.value defined for contact
            try:
                birthday = d.birthday.value
            except AttributeError:
                continue
            # Handle Feb 29 -> use Feb 28
            try:
                birthday_this_year = birthday.replace(year=today.year)
            except ValueError:
                birthday_this_year = birthday.replace(year=today.year, day=28)
            delta_days = (birthday_this_year - today).days
            if 0 < delta_days < 7:
                day_of_week = birthday_this_year.strftime("%A")
                if day_of_week == "Saturday" or day_of_week == "Sunday":
                    day_of_week = "Monday"
                res[day_of_week].append(d.name.value)
        return dict(sorted(res.items(), key=lambda x: BirthdaysPerWeek.weekday_to_number(x[0])))
    
    def output(self, userdict) -> str:
        res = str()
        for k, v in userdict.items():
            value_string = re.sub(r"\]|\[|'", "", str(v))
            res = res + f"{k}: {value_string}\n"
        res = res.rstrip("\n")    
        return res
    
    def __str__(self) -> str:
        return self.output(self.get_birthdays_per_week(self.contacts))
    

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)    

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
        birthday_str = f", birthday: {self.birthday}" if self.birthday is not None else ""
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}{birthday_str}"


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

    def show_birthday(self, record):
        res = None
        if record in self.data:
            res = self.data[record].birthday
        return res

    def get_birthdays_per_week(self):
        return BirthdaysPerWeek(self)


def main():
    # Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    john_record.add_birthday("30.10.2000")
    #book.show_birthday("John")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    jane_record.add_birthday("01.11.2000")
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    #for name, record in book.data.items():
    #    print(record)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")
    john_birthday = book.show_birthday("John")
    print(john_birthday)
    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    birthdays_per_week = book.get_birthdays_per_week()
    print(birthdays_per_week)


    # Пошук конкретного телефону у записі John
    #found_phone = john.find_phone("5555555555")
    #print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

    # Видалення запису Jane
    book.delete("Jane")


if __name__ == "__main__":
    main()
