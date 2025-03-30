import os
import re


def get_host_from_url(url: str):
    match = re.search(r"https?:\/\/([^\/]+)", url)
    return match.group(1)

def sanitize_str(url: str, str_replacement: str):
    url = url.replace("/", str_replacement)
    url = url.replace(":", str_replacement)
    url = url.replace("*", str_replacement)
    url = url.replace("?", str_replacement)
    url = url.replace("<", str_replacement)
    url = url.replace(">", str_replacement)
    url = url.replace("|", str_replacement)
    return url.replace("\\", str_replacement)

def fetch_file_names_in_path(path: str):
    directory = os.fsencode(path)
    return os.listdir(directory)