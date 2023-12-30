import os
import requests
from zipfile import ZipFile
from io import BytesIO
import configparser
import subprocess

def download_and_extract_zip(zip_url, extract_path):
    response = requests.get(zip_url)
    print("Download completed.\nExtracting files...")
    with ZipFile(BytesIO(response.content)) as zip_file:
        zip_file.extractall(extract_path)
    print("All files extracted.\nRunning setup.py ...")

def get_latest_commit_sha(username, repository, branch):
    api_url = f'https://api.github.com/repos/{username}/{repository}/commits/{branch}'
    response = requests.get(api_url)
    return response.json().get('sha', '')

def update_from_github(username, repository, branch, folder, download_path, local_commit_sha):
    global config, response
    base_url = f'https://github.com/{username}/{repository}/archive/{branch}.zip'

    latest_commit_sha = get_latest_commit_sha(username, repository, branch)

    # Check if the local repository is up-to-date

    if local_commit_sha == latest_commit_sha:
        print("Already up to date. No update necessary.")
        exit()

    # Perform the update
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    print("Downloading new version...")

    download_and_extract_zip(base_url, download_path)

    subprocess.run(["python3",f"{local_download_path}/S.O.N.A.R.-main/S.O.N.A.R/setup.py"])
    config['UPDATE']['local_commit_sha'] = get_latest_commit_sha(username,repository,branch)
    response = "Update was installed successfully."


if __name__ == "__main__":
    response = ""
    print("Looking for updates...")

    config = configparser.ConfigParser()
    config.read("sonar.conf")
    
    try:
        github_username = config.get('UPDATE', 'github_username')
        github_repository = config.get('UPDATE', 'github_repository')
        github_branch = config.get('UPDATE', 'github_branch')
        github_folder = config.get("UPDATE", "github_folder")
        local_download_path = config.get("UPDATE", "local_download_path")
        auto_update = config.get("UPDATE","auto_update")
        local_commit_sha = config.get("UPDATE","local_commit_sha")
    except:
        config['UPDATE']['github_username'] = "ShadowFlameFox"
        config['UPDATE']['github_repository'] = "S.O.N.A.R."
        config['UPDATE']['github_branch'] = "main"
        config['UPDATE']['github_folder'] = "S.O.N.A.R"
        config['UPDATE']['local_download_path'] = "DOWNLOAD"
        config['UPDATE']['auto_update'] = "False"
        config['UPDATE']['local_commit_sha'] = None

    try: 
        port = config.get("API","port")
        host = config.get("API","host")
    except:
        config['API']['port'] = 5000
        config['API']['host'] = "127.0.0.1"

    update_from_github(github_username, github_repository, github_branch, github_folder, local_download_path, local_commit_sha)
    print("Updating config...")
    new_config = configparser.ConfigParser()
    new_config.read("DOWNLOAD/S.O.N.A.R.-main/S.O.N.A.R/sonar.conf")
    config['GENERAL']['version'] = new_config["GENERAL"]["version"]

    with open('sonar.conf', 'w') as configfile:
        config.write(configfile)

    print(response)
