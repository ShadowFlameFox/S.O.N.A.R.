import index

def exc(command):
    if command == "exit":
        exit()
    elif "CREATE " in command:
        name = str(command).replace("CREATE ", "")
        msg, value, code = index.create_database(name)
    elif "GET" in command:
        name = str(command).replace("GET ", "")
        attributes = name.split(" ")
        msg, value, code = index.load(attributes[0], attributes[1])
    elif "STORE" in command:
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
    else:
        return "Command not found!"
    if value:
        return value
    else:
        return msg

if __name__ == "__main__":
    while True:
        print(exc(input(": ")))
