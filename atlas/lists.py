# config.py
from pathlib import Path

ASSISTANT_NAME = "Atlas"
GOOGLE_BASE = "https://www.google.com/search?q="

WEBSITES = {
    ("yt","youtube"): "https://www.youtube.com",
    ("gh","github"): "https://github.com",
    ("gg","google"): "https://www.google.com",
    ("rd","reddit"): "https://www.reddit.com",
    ("chatgpt", "gpt"): "https://chatgpt.com/",
}

PROGRAMME = {
    "explorer": "explorer",
    "download": Path.home() / "Downloads",
}