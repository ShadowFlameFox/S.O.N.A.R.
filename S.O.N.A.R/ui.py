import index
import configparser
from termcolor import colored

def exc(command):
    if " -code" in command:
        str(command).replace(" -code","")
        d_code = True
    else:
        d_code = False
    if command == "exit":
        exit()
    elif "CREATE " in command:
        name = str(command).replace("CREATE ", "")
        msg, value, code = index.create_database(name)
    elif "GET" in command:
        name = str(command).replace("GET ", "")
        attributes = name.split(" ")
        msg, value, code = index.load(attributes[0], attributes[1])
    elif command.split(" ")[0] == "STORE":
        name = str(command).replace("STORE ", "")
        attributes = name.split(" ")
        msg, value, code = index.store(attributes[0],attributes[1],attributes[2])
    elif "LIST" in command:
        name = str(command).replace("LIST ", "")
        msg, value, code = index.list_subfolders()
    elif "DELETE_KEY" in command:
        name = str(command).replace("DELETE_KEY ", "")
        attributes = name.split(" ")
        msg, value, code = index.delete_key(attributes[0], attributes[1])
    elif "DELETE_DATABASE" in command:
        name = str(command).replace("DELETE_DATABASE ", "")
        msg, value, code = index.delete_database(name)
    elif command.split(" ")[0] == "TEMP_STORE":
        name = str(command).replace("TEMP_STORE ", "")
        attributes = name.split(" ")
        msg, value, code = index.store_temp(attributes[0],attributes[1],attributes[2])
    elif "CLEAR " in command:
        name = str(command).replace("CLEAR ","")
        msg, value, code = index.clear_temp(name)
    else:
        return "Command not found!"
    if d_code:
        return code
    if value:
        return value
    else:
        return msg

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("sonar.conf")
    version = config.get("GENERAL", "version")
    if version != "0.1.0":
        print(colored("This UI version is deprecated. Some features may not be supported.", "yellow"))
    while True:
        print(exc(input(": ")))
