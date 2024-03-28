import os

def is_folder_empty(folder_path):
    try:
        files = os.listdir(folder_path)
        return len(files) == 0
    except OSError as e:
        print(f"Error reading folder: {folder_path}")
        print(e)
        return False

def delete_folder(folder_path):
    try:
        os.rmdir(folder_path)
        print(f"Folder deleted: {folder_path}")
    except OSError as e:
        print(f"Error deleting folder: {folder_path}")
        print(e)

def check_and_delete_empty_folder(folder_path):
    if is_folder_empty(folder_path):
        delete_folder(folder_path)
    else:
        print(f"Folder not empty: {folder_path}")


all=(os.listdir())
for i in all:
    check_and_delete_empty_folder(i)