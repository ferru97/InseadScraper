import re

def cleanText(text):
    text = text.replace("\n", "").strip()
    return re.sub(' +', ' ', text)