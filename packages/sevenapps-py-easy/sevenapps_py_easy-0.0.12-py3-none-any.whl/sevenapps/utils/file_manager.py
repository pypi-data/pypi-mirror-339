import json
import os
import sys
from datetime import datetime


def check_if_exist_file_in_folder(file_path):
    folder_path, file_name = os.path.split(file_path)

    if os.path.exists(folder_path):
        folder_files = os.listdir(folder_path)

        if file_name in folder_files:
            return True
        else:
            return False
    else:
        return False


def remove_file(file_path):
    folder_path, file_name = os.path.split(file_path)

    if os.path.exists(folder_path):
        folder_files = os.listdir(folder_path)

        if file_name in folder_files:
            file_to_remove = os.path.join(folder_path, file_name)
            os.remove(file_to_remove)
            return True
        else:
            return False
    else:
        return False


def read_json_file(path):
    f = open(path)

    config = json.load(f)

    f.close()

    return config


def rename_file(path, new_name):
    if os.path.exists(path):
        folder_path, file_name = os.path.split(path)
        new_path = os.path.join(folder_path, new_name)
        os.rename(path, new_path)
        print(f"[FILE RENAMED]: The file {file_name} has been renamed as {new_name}.")
    else:
        print("[ERROR]: The specified file does not exist")



def generate_file_name_with_date(file_name):
    return f"{file_name}_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}"

def read_bash_input_parameters():
    if len(sys.argv) > 1:
        return sys.argv[1].lower()

    else:
        return "no_parameter"

