import os
import shutil
from termcolor import colored

def move_file_three_levels_up(file_name):
    # Get the directory of the script
    script_directory = os.path.dirname(os.path.abspath(__file__))

    # Construct the full path of the file to move
    file_path = os.path.join(script_directory, file_name)

    # Check if the file exists
    if not os.path.exists(file_path):
        print(colored(f"Error: File '{file_path}' not found.","red"))
        return

    # Construct the destination directory (three levels above the original file)
    destination_directory = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(file_path))))

    # Construct the destination path
    destination_path = os.path.join(destination_directory, file_name)

    try:
        # Move the file
        shutil.move(file_path, destination_path)
        print(f"File '{file_name}' moved to '{destination_directory}'.")
    except Exception as e:
        print(colored(f"Error: Unable to move the file. {e}","red"))

if __name__ == "__main__":
    move_file_three_levels_up("api.py")
    move_file_three_levels_up("ui.py")
    move_file_three_levels_up("index.py")