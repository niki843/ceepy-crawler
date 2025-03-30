import os


def sanitize_url(url: str):
    url = url.replace("https://", "")
    url = url.replace("http://", "")
    return url.replace("/", "_")

def fetch_file_names_in_path(path: str):
    directory = os.fsencode(path)
    return os.listdir(directory)