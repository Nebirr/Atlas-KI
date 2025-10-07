# web_actions.py
import urllib.parse, webbrowser
import os, sys, subprocess
import re
import unicodedata
from atlas.lists import GOOGLE_BASE, WEBSITES



def build_google_search_url(query: str) -> str:
    q = urllib.parse.quote_plus(query.strip())
    return f"{GOOGLE_BASE}{q}"

def normalize_ascii(s: str) -> str:
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii").lower().strip()

def open_url_system_default(url: str) -> bool:
    try:
        if sys.platform.startswith("win"):
            os.startfile(url)  # nutzt den Standard-Handler für https
            return True
        elif sys.platform == "darwin":
            subprocess.run(["open", url], check=False)
            return True
        else:
            subprocess.run(["xdg-open", url], check=False)
            return True
    except Exception:
        return webbrowser.open(url)


def resolve_website_alias(term: str) -> str | None:
    t = term.strip().lower()

    # 1) exakter String-Key
    if t in WEBSITES:
        return WEBSITES[t]

    # 2) Tuple-/Iterable-Keys
    for k, v in WEBSITES.items():
        if isinstance(k, (tuple, list, set)):
            if t in k:
                return v
    return None

def handle_search(task_lc: str) -> bool:
    t = normalize_ascii(task_lc)
    # English triggers
    if t.startswith(("search for ", "google ", "search ")):
        # remove leading keywords
        q = re.sub(r"^(search for|search|google)\s+", "", t, flags=re.I).strip()
        if not q:
            print("What should I search for?")
            return True
        url = f"https://www.google.com/search?q={q.replace(' ', '+')}"
        webbrowser.open(url)
        print(f"Searching for: {q}")
        return True
    return False

def open_website(task_lc: str) -> bool:
    t = normalize_ascii(task_lc)
    if not t.startswith("open "):
        return False

    rest = t.split("open", 1)[1].strip()
    if not rest:
        print("Please specify a website to open (alias or URL).")
        return True

    # 1) Aliasse (inkl. Tuple-Keys) auflösen
    alias_url = resolve_website_alias(rest)
    if alias_url:
        open_url_system_default(alias_url)
        print(f"Opening: {alias_url}")
        return True

    # 2) Domain ohne Schema ? https:// ergänzen
    if "." in rest and not re.match(r"^https?://", rest):
        rest = "https://" + rest
        open_url_system_default(rest)
        print(f"Opening: {rest}")
        return True

    # 3) Enthält Leerzeichen ? eher Suchbegriff ? Google-Suche
    if " " in rest and not re.match(r"^https?://", rest):
        search_url = build_google_search_url(rest)
        open_url_system_default(search_url)
        print(f"No direct match ? Searching: {rest}\n{search_url}")
        return True

    # 4) Fallback: direkte URL öffnen
    open_url_system_default(rest)
    print(f"Opening: {rest}")
    return True