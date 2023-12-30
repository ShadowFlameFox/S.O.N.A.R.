import os
import requests
from zipfile import ZipFile
from io import BytesIO
import configparser
import subprocess
import time

def download_and_extract_zip(zip_url, extract_path):
    response = requests.get(zip_url)
    print("Download completed.\nExtracting files...")
    with ZipFile(BytesIO(response.content)) as zip_file:
        zip_file.extractall(extract_path)
    print("All files extracted.\nRunning setup.py ...")

def get_latest_commit_sha():
    api_url = f'https://api.github.com/repos/ShadowFlameFox/S.O.N.A.R./commits/main'
    response = requests.get(api_url)
    return response.json().get('sha', '')

def update_from_github():
    global config, response
    base_url = f'https://github.com/ShadowFlameFox/S.O.N.A.R./archive/main.zip'

    if not os.path.exists("DOWNLOAD"):
        os.makedirs("DOWNLOAD")

    print("Downloading new version...")

    download_and_extract_zip(base_url, "DOWNLOAD")

    subprocess.run(["python3",f"DOWNLOAD/S.O.N.A.R.-main/S.O.N.A.R/setup.py"])
    response = "Installation successful."


if __name__ == "__main__":
    subprocess.run(["python3","-m","pip","install","flask","termcolor","requests"])
    subprocess.run(["mkdir", "DB"])
    update_from_github()
    print("Creating configuration file...")
    new_config = configparser.ConfigParser()
    new_config.read("DOWNLOAD/S.O.N.A.R.-main/S.O.N.A.R/sonar.conf")
    with open('sonar.conf', 'w') as configfile:
        new_config.write(configfile)

    config = configparser.ConfigParser()
    config.read("sonar.conf")
    config['UPDATE']['local_commit_sha'] = get_latest_commit_sha()
    with open('sonar.conf', 'w') as configfile:
        config.write(configfile)
    print("Configuration file created.")
    print("Removing the installation directory...")
    subprocess.run(["rm","-r", "DOWNLOAD"])
    print("Installation directory has been removed.")

    print(response)