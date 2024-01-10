from collections import UserDict
from time import strptime
from datetime import date, datetime
import pickle
from pathlib import Path


class NotCorrectData(Exception):
    pass

class NotCorrectPhone(Exception):
    pass

class Field:
    def __init__(self, value):
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    def __str__(self) -> str:
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        self._value = None
        self.value = value
        super().__init__(self._value)

    @property
    def value(self):
        return self.value
    
    @Field.value.setter
    def value(self, value):
        self._value = value.title()


class Phone(Field):
    def __init__(self, value):
        self._value = None
        self.value = value
        super().__init__(self._value)

    @property
    def value(self):
        return self._value
    
    @Field.value.setter
    def value(self, phone):
        if phone.isdigit() and len(phone) == 10:
            self._value = phone
        else:
            raise NotCorrectPhone

    def validate(self, phone):
        if phone.isdigit() and len(phone) == 10:
            return True
        return False

class Birthday(Field):
    def __init__(self, value):
        self._value = None
        self.value = value
        super().__init__(self._value)

    @property
    def value(self):
        return self._value
    
    @Field.value.setter
    def value(self, value):
        if value == None:
            self._value = None
        else:
            try:
                strptime(value, '%d-%m-%Y')
                self._value = value
            except ValueError:
                raise NotCorrectData

class Record():
    def __init__(self, name, date=None):
        self.name = Name(name)  # Mandatory
        self.phones = []
        self.date = Birthday(date)

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def days_to_birthday(self):
        if self.date.value != None:
            today = date.today()
            bdat = datetime.strptime(self.date.value, '%d-%m-%Y')
            birthday = datetime(year=today.year, month=bdat.month, day=bdat.day)
            curdat = datetime(year=today.year, month=today.month, day=today.day)
            count = (curdat - birthday).days
            count = count if count > 0 else abs(count)
            return f"{count} days left to birthday."
        else:
            return f"Birthday data is misssing."

    def edit_phone(self, phone, phone_new):
        # phone_obj = self.find_phone(phone)
        phone_obj: Phone = self.find_phone(phone)
        if phone_obj and phone_obj.validate(phone_new):
            phone_obj.value = phone_new
        else:
            raise ValueError

    def remove_phone(self, phone_r):
        p_obj = self.find_phone(phone_r)
        if p_obj:
            self.phones.remove(p_obj)

    def find_phone(self, phone_f):
        for phone in self.phones:
            if phone.value == phone_f: return phone

    def __str__(self):
        str_dat = f"; birthday: {self.date.value}" if self.date.value != None else ""
        return f"Name: {self.name.value}; phones: {'; '.join(p.value for p in self.phones)} {str_dat}"
    

class AddressBook(UserDict):
    def __init__(self):
        # self.list_items = []
        self.list_count = 0
        self.data = {}
        self.__abook_file = "book_file.bin"

    def add_record(self, value):
        # self.data[value.name.value] = value.phones
        self.data[value.name.value] = value

    def find(self, name):
        if name in self.data.keys():
            record = Record(name)
            record.phones = self.data[name]
            return self.data.get(name)
        else:
            return None

    def delete(self, name):
        if name in self.data.keys():
            self.data.pop(name)

    def list_creator(self):
        self.list_items = []
        for item in self.data.values():
            self.list_items.append(item)

        self.list_count = len(self.list_items)

    def iterator(self, from_el=0, to_el=2):
        if self.list_count > 0 and from_el < self.list_count:
            return (x for x in self.list_items[from_el:to_el])

    def serialization(self):
        with open(self.__abook_file, "wb") as fh:
            pickle.dump(self.data, fh)

    def check_file_exist(self):
        return Path(self.__abook_file).exists()

    def unserialization(self):
        if self.check_file_exist():
            with open(self.__abook_file, "rb") as fh:
                self.data = pickle.load(fh)
            return self.data

    def search(self, str):
        searched_items = {}
        for val, key in self.data.items():
            if val.find(str) != -1:
                searched_items.update({val: key})
                continue
            for phone in key.phones:
                if phone.value.find(str) != -1:
                    searched_items.update({val: key})
        return searched_items if len(searched_items) > 0 else 0

    def help(self):
        return 

def main():
    abook = AddressBook()
    john_record = Record("John", "12-03-1999")
    john_record.add_phone("0962455835")
    john_record.add_phone("7777777777")
    abook.add_record(john_record)

    count_days_to_birthday = john_record.days_to_birthday()
    print(count_days_to_birthday)


    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    abook.add_record(jane_record)
    count_days_to_birthday = jane_record.days_to_birthday()
    print(count_days_to_birthday)

    bill_record = Record("Bill", "11-02-2005")
    bill_record.add_phone("0502455835")
    bill_record.add_phone("7775577777")
    abook.add_record(bill_record)

    steve_record = Record("Steve", "05-11-2000")
    steve_record.add_phone("0702777835")
    steve_record.add_phone("7775577887")
    abook.add_record(steve_record)

    eva_record = Record("Eva", "01-07-1987")
    eva_record.add_phone("0770277785")
    eva_record.add_phone("7773377887")
    abook.add_record(eva_record)

    for name, record in abook.data.items():
        print(f"Name: {name}, record: {record}")

    print("-"*30)
    abook.list_creator()

    items = abook.iterator()
    for item in items:
        print(f"list: {item}")
    print("-"*30)   

    items = abook.iterator(2,4)
    for item in items:
        print(f"list: {item}") 
    print("-"*35) 

    items = abook.iterator(4,6)
    for item in items:
        print(f"list: {item}")
    print("-"*35) 

    john = abook.find("John")
    if john != None:
        john.edit_phone("0962455835", "1112223333")
        found_phone = john.find_phone("1112223333")
        found_phone = john.find_phone("0962455835")
        print(f"{john.name}: {found_phone}") 
        john.edit_phone("7777777777", "7777777778")

    abook.delete("Jane")

    for name, record in abook.data.items():
        print(f"Name: {name}, record: {record}")

if __name__ == "__main__":
    main()