import re


def deal_title(title: str) -> str:
    title = re.sub("&.*?;", "", title, flags=re.IGNORECASE)
    title = re.sub("<[a-z|A-Z].*?'>", "", title, flags=re.IGNORECASE)
    title = re.sub("<[a-z|A-Z].*?\">", "", title, flags=re.IGNORECASE)
    return title
