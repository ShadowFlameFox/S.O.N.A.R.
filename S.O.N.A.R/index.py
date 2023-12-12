import json
import os
import shutil

def save_data(data, file):
    with open(f"{file}.json", "w", encoding="utf-8") as f:
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
    subfolder_path = os.path.join(script_directory, f"DB/{folder_name}")

    if not os.path.exists(subfolder_path):
        os.makedirs(subfolder_path)
        return f"A database named '{folder_name}' has been created successfully.", None,200
    else:
        return f"A database named '{folder_name}' already exists.", None, 304
    
def store(database, key, value):
    try: 
        save_data(json.loads(value), f"DB/{database}/{key}")
        return f"The value was updated successfully.", None, 200
    except FileNotFoundError:
        return f"Database '{database}' not found.", None, 404

def load(database, key):
    try:
        with open(f"DB/{database}/{key}.json", "r", encoding="utf-8") as f:
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
        os.remove(os.path.join(script_directory, f"DB/{database}/{key}.json"))
        return f"The following key has been deleted: '{key}'", None, 200
    except FileNotFoundError:
        return f"The following key doesn't exsist: '{key}'", None, 404

def delete_database(database):
    try:
        script_directory = os.path.dirname(os.path.abspath(__file__))
        subfolder_path = os.path.join(script_directory, f"DB/{database}")
        shutil.rmtree(subfolder_path)
        return(f"Database '{database}' deleted successfully."), None, 200
    except FileNotFoundError:
        return(f"Database '{database}' not found."), None, 404
    except PermissionError:
        return(f"Permission error: Unable to delete database '{database}'."), None, 401
    except Exception as e:
        return(f"An error occurred: {e}"), None, 500

if __name__ == "__main__":
    pass
