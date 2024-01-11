import address_book_lib as abl
import messages_settings as message
import classes.exceptions as ex
from messages_settings import MESSAGES, EXIT_COMMANDS, WARNING_MESSAGES, COMMAND_HANDLER_DESCRIPTION

contacts_book = abl.AddressBook()

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
        except ex.NotCorrectData as err:
            return message_warging(f"Error: {WARNING_MESSAGES['not_correct_data']}")
        except ex.NotCorrectPhone as err:
            return message_warging(f"Error: {WARNING_MESSAGES['not_correct_phone']}")
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
    count = len(com)
    if count < 3:
        raise ValueError(WARNING_MESSAGES["name_phone"])  

    record_is = contacts_book.find(com[1])
    if record_is == None:
        if count > 3:
            record = abl.Record(com[1], com[2])
            record.add_phone(com[3])
        else:
            record = abl.Record(com[1])
            record.add_phone(com[2])
        contacts_book.add_record(record)
        return message_notice(MESSAGES[com[0]])
    else:
        record_is.add_phone(com[2])
        contacts_book.add_record(record_is)
        return message_notice(MESSAGES[com[0]+"_more"])


def contacts_book_fullness():
    if len(contacts_book) == 0:
        return message_warging(WARNING_MESSAGES["contacts_book_empty"])
    else:
        return 1  


def presence_name(com):
    contact = contacts_book.find(com[1])
    if contact == None:
        return message_warging(WARNING_MESSAGES["missing_name"])
    else:
        return contact


def show_all(com, search=None):
    if search != None:
        iter_Item = search
        message = "show_found"
    else:
        cont = contacts_book_fullness()
        if cont != 1: return cont
        
        iter_Item = contacts_book
        message = com

    contacts = ''
    contacts += message_notice(MESSAGES[message])
    for val in iter_Item.values():
        contacts += '\n' + message_notice(f"{val}", BOLD)
    return contacts


@input_error
def phone(com):
    cont = contacts_book_fullness()
    if cont != 1: return cont

    if len(com) < 2:
        raise ValueError(WARNING_MESSAGES["name"])
    name_is = presence_name(com)
    if name_is != None:
        return message_notice(f"{MESSAGES[com[0]]}{contacts_book[com[1]]}", BOLD)


@input_error
def change(com):
    if len(com) < 4:
        raise ValueError(WARNING_MESSAGES["name_phone"])
    name_is = presence_name(com)
    if name_is != None:
        name_is.edit_phone(com[2], com[3])
        return message_notice(MESSAGES[com[0]])


@input_error
def iter(com):
    contacts_book.list_creator()
    count = len(com)
    if count == 3:
        items = contacts_book.iterator(int(com[1]), int(com[2]))
    else:
        items = contacts_book.iterator()
        
    if items != None:
        contacts = ''
        contacts += message_notice(MESSAGES[com[0]])            
        for item in items:
            contacts += '\n' + message_notice(f"{item}", BOLD)
        return contacts
    else:
        return message_warging(WARNING_MESSAGES["iter_no_result"])


@input_error
def delete(com):
    res = contacts_book.find(com[1])
    if res == None:
        return message_warging(WARNING_MESSAGES["missing_name"])
    else:
        contacts_book.delete(com[1])
        return message_warging(MESSAGES["delete"])

    
@input_error
def search(com):
    res = contacts_book.search(com[1])
    if res != 0:
        return show_all("show_all", res)
    else:
        return message_warging(WARNING_MESSAGES["show_found_empty"])


@input_error
def daysbir(com):
    contact = contacts_book.find(com[1])
    if contact == None:
        return message_warging(WARNING_MESSAGES["missing_name"])
    else:
        res = contact.days_to_birthday()
        return message_notice(f"{res}", BOLD)

@input_error
def help(com):
    res = ""
    for command in COMMAND_HANDLER.keys():
        # res += f"Command: {command}- description: {COMMAND_HANDLER_DESCRIPTION[command]}\n"
        res += message_notice(f"Command: {command}", GREEN)
        res += message_notice(f"- description: {COMMAND_HANDLER_DESCRIPTION[command]}\n", BOLD)
    return res


COMMAND_HANDLER = {
    "hello": message,
    "add": add,
    "change": change,
    "phone": phone,
    "show all": show_all,
    "iter": iter,
    "search": search,
    "delete": delete,
    "daysbir": daysbir,  # Count days to bithday
    "help": help
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
    contacts_book.unserialization()
    while True:
        user_input = input("Input command >>> ")
        user_input = user_input.strip().lower()
        if user_input in EXIT_COMMANDS:
            print(exit(MESSAGES[user_input]))
            contacts_book.serialization()
            break
        res = parsing(user_input)
        print(res)


if __name__ == "__main__":
    main()
