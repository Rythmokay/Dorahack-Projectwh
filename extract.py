import re

def find_urls(text):
    url_regex = r'https?://\S+'
    return re.findall(url_regex, text)
