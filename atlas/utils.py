# utils.py
def take_one(text: str, keywords: list[str]) -> bool:
    return any(word in text for word in keywords)

def normalize(text: str) -> str:
    return (text.lower().strip()
            .replace("ä","ae").replace("ö","oe").replace("ü","ue"))