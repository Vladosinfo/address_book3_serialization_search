contacts_book = {}

MESSAGES = {
    "hello": "How can I help you?",
    "good bye": "Good bye!",
    "close": "Good bye!",
    "exit": "Good bye!",
    "add": "Your contact has been added",
    "change": "Your contact has been changed",
    "phone": "It's your phone number: ",
    "show_all": "These are all contacts:"
}
EXIT_COMMANDS = ["good bye", "close", "exit"]
WARNING_MESSAGES = {
    "correct_command": "Enter correct command",
    "name": "Enter user name",
    "name_phone": "Give me name and phone please",
    "missing_name": "This name is missing in contact book",
    "contacts_book_empty": "Contacts book is empty yet."
}
RED = "\033[91m"
GREEN = "\033[92m"
BOLD = '\033[1m'
RESET = "\033[0m"


def message_notice(notice, color = None):
    color = color or GREEN
    return f"{color} {notice} {RESET}"
    

def message_warging(warning):
    return f"{RED} {warning} {RESET}"


def input_error(func):
    def wrapper(user_input):
        try:
            return func(user_input)
        except KeyError as err:
            return message_warging(f"Error: {err}")
        except ValueError as err:
            return message_warging(f"Error: {err}")
        except IndexError as err:
            return message_warging(f"Error: {err}")
    return wrapper


def message(mes):
    return message_notice(MESSAGES[mes[0]])


def exit(mes):
    return message_notice(mes)


@input_error
def error(err):
    raise ValueError(WARNING_MESSAGES["correct_command"])


@input_error
def add(com):
    if len(com) < 3:
        raise ValueError(WARNING_MESSAGES["name_phone"])      
    contacts_book[com[1]] = com[2]
    return message_notice(MESSAGES[com[0]])


def contacts_book_fullness():
    if len(contacts_book) == 0:
        return message_warging(WARNING_MESSAGES["contacts_book_empty"])
    else:
        return 1  


def presence_name(com):
    if contacts_book.get(com[1]) == None:
        return message_warging(WARNING_MESSAGES["missing_name"])
    else: return True


def show_all(com):
    cont = contacts_book_fullness()
    if cont != 1: return cont

    contacts = ''
    contacts += message_notice(MESSAGES[com])
    for key, val in contacts_book.items():
        contacts += '\n' + message_notice(f"Name: {key.capitalize()} | phone: {val}", BOLD)
    return contacts


@input_error
def phone(com):
    cont = contacts_book_fullness()
    if cont != 1: return cont

    if len(com) < 2:
        raise ValueError(WARNING_MESSAGES["name"])
    if presence_name(com): 
        return message_notice(f"{MESSAGES[com[0]]}{contacts_book[com[1]]}", BOLD)


@input_error
def change(com):
    cont = contacts_book_fullness()
    if cont != 1: return cont
     
    if len(com) < 3:
        raise ValueError(WARNING_MESSAGES["name_phone"])
    if presence_name(com):
        contacts_book[com[1]] = com[2]
        return message_notice(MESSAGES[com[0]])


COMMAND_HANDLER = {
    "hello": message,
    "add": add,
    "change": change,
    "phone": phone,
    "show all": show_all
}


def command_handler(com):
    handler = COMMAND_HANDLER.get(com[0], error)
    return handler(com)


@input_error
def parsing(user_input):
    if user_input.startswith("show all"):
        return show_all("show_all")
    return command_handler(user_input.split(" "))


def main():
    while True:
        user_input = input("Input command >>> ")
        user_input = user_input.strip().lower()
        if user_input in EXIT_COMMANDS:
            print(exit(MESSAGES[user_input]))
            break
        res = parsing(user_input)
        print(res)


if __name__ == "__main__":
    main()
