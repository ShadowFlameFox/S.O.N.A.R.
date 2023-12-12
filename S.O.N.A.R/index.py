import json
import os

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
    subfolder_path = os.path.join(script_directory, f"DB\\{folder_name}")

    if not os.path.exists(subfolder_path):
        os.makedirs(subfolder_path)
        return f"A database named '{folder_name}' has been created successfully."
    else:
        return f"A database named '{folder_name}' already exists."
    
def store(database, key, value):
    save_data(json.loads(value), f"DB\\{database}\\{key}")
    return f"The value was updated successfully."

def load(database, key):
    return load_data(f"DB\\{database}\\{key}")

def list_subfolders():
    script_directory = os.path.dirname(os.path.abspath(__file__))
    subfolder_path = os.path.join(script_directory, f"DB\\")
    subfolders_list = []
    try:
        subfolders = [f.name for f in os.scandir(subfolder_path) if f.is_dir()]
        
        if subfolders:
            for subfolder in subfolders:
                subfolders_list.append(subfolder)
            return subfolders_list
        else:
            return "No database found."

    except FileNotFoundError:
        return f"Fatal error: The main directory was not found!"

def delete_key(database, key):
    script_directory = os.path.dirname(os.path.abspath(__file__))
    os.remove(os.path.join(script_directory, f"DB\\{database}\\{key}.json"))
    return f"The following key has been deleted: '{key}'"

if __name__ == "__main__":
    pass