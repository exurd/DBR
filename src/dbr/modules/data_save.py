import json
import os

DATA_FOLDER = None
CHECKED_PLACES = []


def get_data_file_path(root_folder):
    """
    Sets DATA_FOLDER to a specifed root folder.
    """
    global DATA_FOLDER
    DATA_FOLDER = os.path.join(root_folder)
    os.makedirs(DATA_FOLDER, exist_ok=True)
    print(f"data_folder: [{DATA_FOLDER}]")
    return DATA_FOLDER


def load_data(filename):
    """
    Load data from a JSON file.
    """
    if DATA_FOLDER is None:
        data_file_path = os.path.join(filename)
    else:
        data_file_path = os.path.join(DATA_FOLDER, filename)
    if os.path.exists(data_file_path) and os.path.getsize(data_file_path) > 0:
        with open(data_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            f.close()
    else:
        data = []
    return data


def save_data(data, filename):
    """
    Saves data to a JSON file.
    """
    if DATA_FOLDER is None:
        data_file_path = os.path.join(filename)
    else:
        data_file_path = os.path.join(DATA_FOLDER, filename)

    with open(data_file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4, sort_keys=True)
        f.close()


def init(root_folder):
    """
    Initialises variables from JSON files.
    """
    global CHECKED_PLACES

    get_data_file_path(root_folder)
    CHECKED_PLACES = load_data("checked_places.json")
