import re

def detect_language(text: str) -> str:
    if not text: return "Unknown"
    if re.search(r'[\u0C00-\u0C7F]', text): return "Telugu"
    elif re.search(r'[\u0900-\u097F]', text): return "Hindi"
    elif re.search(r'[a-zA-Z]', text): return "English"
    return "Unknown"