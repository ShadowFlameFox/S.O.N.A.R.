import json
import os
import shutil
import subprocess
import configparser
import time

config = configparser.ConfigParser()
config.read("sonar.conf")
auto_update = config.get("UPDATE", "auto_update")
if auto_update == "True":
    subprocess.run(["python3","update.py"])
time.sleep(.2)

def save_data(data, file):
    try:
        with open(f"{file}.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except FileNotFoundError:
        with open(f"{file}.json", "w+", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

def load_data(file):
    try:
        with open(f"{file}.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        return {}

def get_object(obj, file):
    data = load_data(file)
    try:
        return data[obj]
    except:
        return None
        
def update_object(obj, new_value, file):
    data = load_data(file)
    data[obj] = new_value
    save_data(data, file)


def create_database(folder_name):
    script_directory = os.path.dirname(os.path.abspath(__file__))
    subfolder_path = os.path.join(script_directory, f"DB/{folder_name}.db")

    if not os.path.exists(subfolder_path):
        os.makedirs(subfolder_path)
        subfolder_path = os.path.join(script_directory, f"DB/{folder_name}.db/temp")
        os.makedirs(subfolder_path)
        subfolder_path = os.path.join(script_directory, f"DB/{folder_name}.db/conf")
        os.makedirs(subfolder_path)
        open(f"DB/{folder_name}.db/conf/{folder_name}.conf", "w+")
        #setup the file
        return f"A database named '{folder_name}' has been created successfully.", None,201
    else:
        return f"A database named '{folder_name}' already exists.", None, 304
    
def store(database, key, value):
    data = load_data(f"DB/{database}.db/{key}.json")

    objects = str(value).split(";;")
    
    for object in objects:
        key_value_pair = object.split("::")
        if len(key_value_pair) == 2:
            data[key_value_pair[0]] = key_value_pair[1]
        else:
            return f"Invalid key-value pair: {object}. Expected format: 'key::value'", None, 400
    save_data(data, f"DB/{database}.db/{key}")
    return f"The objects were stored in the following key: '{key}'", None, 201

def load(database, key):
    try:
        with open(f"DB/{database}.db/{key}.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            return None, data, 200
    except FileNotFoundError:
        return "Database or key not found", None, 404
    

def list_subfolders():
    script_directory = os.path.dirname(os.path.abspath(__file__))
    subfolder_path = os.path.join(script_directory, f"DB/")
    subfolders_list = []
    try:
        subfolders = [f.name for f in os.scandir(subfolder_path) if f.is_dir()]
        
        if subfolders:
            for subfolder in subfolders:
                subfolders_list.append(subfolder)
            return None, subfolders_list, 200
        else:
            return "No database found.", None, 404

    except FileNotFoundError:
        return f"Fatal error: The main directory was not found!", None, 404

def delete_key(database, key):
    try:
        script_directory = os.path.dirname(os.path.abspath(__file__))
        os.remove(os.path.join(script_directory, f"DB/{database}.db/{key}.json"))
        return f"The following key has been deleted: '{key}'", None, 200
    except FileNotFoundError:
        return f"The following key doesn't exsist: '{key}'", None, 404

def delete_database(database):
    try:
        script_directory = os.path.dirname(os.path.abspath(__file__))
        subfolder_path = os.path.join(script_directory, f"DB/{database}.db")
        shutil.rmtree(subfolder_path)
        return(f"Database '{database}' deleted successfully."), None, 200
    except FileNotFoundError:
        return(f"Database '{database}' not found."), None, 404
    except PermissionError:
        return(f"Permission error: Unable to delete database '{database}'."), None, 400
    except Exception as e:
        return(f"An error occurred: {e}"), None, 500

def store_temp(database, key, value):
    data = load_data(f"DB/{database}.db/temp/{key}.json")

    objects = str(value).split(";;")
    
    for object in objects:
        key_value_pair = object.split("::")
        if len(key_value_pair) == 2:
            data[key_value_pair[0]] = key_value_pair[1]
        else:
            return f"Invalid key-value pair: {object}. Expected format: 'key::value'", None, 400
    save_data(data, f"DB/{database}.db/temp/{key}")
    return f"The objects were stored in the following temporary key: '{key}'", None, 201

def clear_temp(database):
    try:
        script_directory = os.path.dirname(os.path.abspath(__file__))
        subfolder_path = os.path.join(script_directory, f"DB/{database}.db/temp")
        shutil.rmtree(subfolder_path)
        subfolder_path = os.path.join(script_directory, f"DB/{database}.db/temp")
        os.makedirs(subfolder_path)
        return(f"All temporary keys from '{database}' have been successfully deleted."), None, 200
    except FileNotFoundError:
        return(f"Database '{database}' not found."), None, 404
    except PermissionError:
        return(f"Permission error: Unable to delete temporary keys from '{database}'."), None, 400
    except Exception as e:
        return(f"An error occurred: {e}"), None, 500

if __name__ == "__main__":
    print("Use 'screen -AdmS sonar python3 api.py' or 'python3 ui.py' to start S.O.N.A.R.")
