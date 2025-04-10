import os

def file_exists(path):
    return os.path.isfile(path)

def get_extension(path):
    return os.path.splitext(path)[1].lower()
