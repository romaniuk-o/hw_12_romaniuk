from datetime import datetime, date
from collections import UserDict
import shelve

#  _______Функція декоратор____________


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except KeyError:
            return('Enter user name')
        except ValueError:
            return('Value is not correct')
        except IndexError:
            return('Give me name and phone please')
        except TypeError:
            return('Enter the correct command')
        except BirthdayError:
            return('Enter date in format YYYY-MM-DD')
        except NumberOfLinesError:
            return('Phone book has no so many abonents')
    return wrapper


class Field:
    def __init__(self, value):
        self.__value = None
        self.value = value

    def __str__(self, value):
        return f'{value}'

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)

    @Field.value.setter
    def value(self, value):
        codes_operators = ["067", "068", "096", "097", "098",
                           "050", "066", "095", "099", "063", "073", "093"]
        new_value = (value.strip()
                     .removeprefix('+')
                     .replace("(", '')
                     .replace(")", '')
                     .replace("-", ''))
        if new_value[:2] == '38' and len(new_value) == 12 and new_value[2:5] in codes_operators:
            Field.value.fset(self, new_value)
        else:
            raise ValueError


@ input_error
class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)

    @Field.value.setter
    def value(self, value):
        if bool(date.fromisoformat(value)):

            Field.value.fset(self, value)
        else:
            raise BirthdayError


class BirthdayError(Exception):
    pass


class NumberOfLinesError(Exception):
    pass


class Record():
    def __init__(self, name: Name, phones: Phone = [], birthday: Birthday = '-') -> None:
        self.name = name
        self.phone_lst = phones
        self.birthday = birthday

    def phone_add(self, phone):
        self.phone_lst.append(phone)

    def phone_del(self, phone):
        self.phone_lst.remove(phone)

    def phone_change(self, old_phone, new_phone):
        self.phone_lst.remove(old_phone)
        self.phone_lst.append(new_phone)

    def birthday_add(self, birthday):
        self.birthday = birthday

    def days_to_birthday(self, birthday) -> int:
        b_date = datetime.strptime(birthday, '%Y-%m-%d')
        c_date = datetime.today()
        if c_date.timestamp() > datetime(year=c_date.year, month=b_date.month, day=b_date.day).timestamp():
            next_birthday = datetime(
                year=c_date.year + 1, month=b_date.month, day=b_date.day)
        else:
            next_birthday = datetime(
                year=c_date.year, month=b_date.month, day=b_date.day)
        return (next_birthday.date() - datetime.today().date()).days

    def __repr__(self):
        return f"Name: {self.name} | Phone: {str(self.phone_lst)} | Birthday: {self.birthday}  "


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def iterator(self, n):
        i = 0
        list_from_dict = [f'{k}:{v}' for k, v in self.data.items()]
        while i <= len(self.data):

            if (len(self.data) - i) > n:
                yield '\n'.join([str(list_from_dict[i]) for i in range(i, i+n)])
                i += n
            else:
                _ = len(self.data)-i
                yield '\n'.join([str(list_from_dict[i]) for i in range(i, i+_)])

    def find_symbols(self, symbol) -> int:
        count = 0
        for v in self.data.values():
            if (v.name.find(symbol) != -1) or (v.birthday.find(symbol) != -1) or (','.join(v.phone_lst).find(symbol) != -1):
                count += 1
                print(f"| {v} | ")

        if count == 0:
            return "Nothing found"
        else:
            return "Search complete"

    def __repr__(self):
        for k, v in self.data.items():
            print(f"| {v} | ")
        return f'end of phone book'

 # ______Функції - ключові слова____________________


phone_book = AddressBook()


@ input_error
def hello(*args) -> str:
    return 'How can I help you?'


@ input_error
def exit(*args) -> str:
    return 'Bye!'


@ input_error
def add(*args) -> str:
    name = Name(args[0])
    phone = Phone(args[1])
    if name.value in phone_book:
        if phone.value in phone_book[name.value].phone_lst:
            return f'such number alreadey is!!!'
        else:
            phone_book[name.value].phone_add(phone.value)
            return f'Number {phone.value} added to user name {name.value} !!!'
    else:
        phone_book[name.value] = Record(name.value, [phone.value])
        return 'Contact add successful!'


@ input_error
def birthday_add(*args) -> str:
    name = Name(args[0])
    birthday = Birthday(args[1])
    if name.value in phone_book:
        phone_book[name.value].birthday_add(birthday.value)

    else:
        phone_book[name.value] = Record(name.value, [], birthday.value)
    return f'{name.value} birthday is {birthday.value}!'


@ input_error
def days_to(*args):
    name = Name(args[0])
    if name.value in phone_book:
        birth = phone_book[name.value].birthday
        _ = phone_book[name.value].days_to_birthday(birth)
        return f'To {name.value} birthday is {_} days'
    else:
        return f'{name.value} is not in phone book'


@ input_error
def find_symb(*args):
    return phone_book.find_symbols(args[0])


@ input_error
def show_all(*args):
    return phone_book


@ input_error
def number_of_records(*args):
    n = int(args[0])

    if n > len(phone_book):
        raise NumberOfLinesError
    else:
        _ = phone_book.iterator(n)
        i = 1
        while ((n*i)-n) < len(phone_book):
            i += 1
            print(next(_))

        return f'end of phone book'


@ input_error
def change(*args) -> str:
    name = args[0]
    old_phone = args[1]
    new_phone = args[2]
    if name in phone_book:
        phone_book[name].phone_change(old_phone, new_phone)
        return f'Phone number {old_phone} changed on {new_phone} successful!'
    else:
        return f'Contact with name {name} not found!'


@ input_error
def phone(*args) -> str:
    return phone_book[args[0]].phone_lst


@ input_error
def wrong(*args) -> str:
    return 'Unknown command'


#  Функція command_parser - парсер команд
# ___________________________________________________________________________________


COMMAND_DICT = {hello: ['hello'], phone: ['phone'], change: ['change'],  exit: ['exit', 'close', 'good bye'],
                add: ['add'], show_all: ["show all", "show"], birthday_add: ['birthday'], number_of_records: ['records'], days_to: ['days to birthday'], find_symb: ['find']}


# @input_error
def command_parser(comm: str):
    for k, v in COMMAND_DICT.items():
        for i in v:
            if comm.lower().startswith(i.lower()):
                return k, comm[len(i):].strip().split(' ')
    else:
        return wrong, []
 # _____________________________________________________________________________


filename = 'phone_book_db'


def main():
    while True:
        user_input = input('Please type command: ')
        command, data = command_parser(user_input)
        result = command(*data)
        print(result)
        if command == exit:
            with shelve.open(filename) as db:
                for k, v in phone_book.items():
                    db[k] = v
            break


if __name__ == '__main__':
    with shelve.open(filename) as states:
        for key in states:
            phone_book[key] = states[key]

    main()
