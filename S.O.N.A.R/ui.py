import index

def exc(command):
    if command == "exit":
        exit()
    elif "CREATE " in command:
        name = str(command).replace("CREATE ", "")
        print(index.create_database(name))
    elif "GET" in command:
        name = str(command).replace("GET ", "")
        attributes = name.split(";")
        print(index.load(attributes[0], attributes[1]))
    elif "STORE" in command:
        name = str(command).replace("STORE ", "")
        attributes = name.split(";")
        print(index.store(attributes[0],attributes[1],attributes[2]))
    elif "LIST" in command:
        name = str(command).replace("LIST ", "")
        print(index.list_subfolders())
    elif "DELETE_KEY" in command:
        name = str(command).replace("DELETE_KEY ", "")
        attributes = name.split(";")
        print(index.delete_key(attributes[0], attributes[1]))

if __name__ == "__main__":
    while True:
        exc(input(": "))