from pathlib import Path
import os

def get_files_list(folder_path):
    return [p for p in Path(folder_path).iterdit() if p.is_file()]

def get_files(folder):
    files = []
    for file in Path(folder).iterdir():
        if file.is_file():
            files.append(file)
    return files


def delete_file(folder, file_name):
    os.remove(os.path.join(folder, file_name))