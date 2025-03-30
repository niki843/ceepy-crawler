import re


def get_host_from_url(url: str):
    match = re.search(r"https?:\/\/([^\/]+)", url)
    return match.group(1)
