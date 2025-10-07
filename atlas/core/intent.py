from __future__ import annotations
from dataclasses import dataclass
from enum import Enum, auto
import unicodedata

import re

from atlas.help_cmd import matches_help
from atlas.intern_tasks import matches_systeminfo 
from atlas.lists import PROGRAMME, WEBSITES

class Intent(Enum):
    HELP = auto()
    SYSTEMINFO = auto()
    TIME_OR_DATE = auto()
    START_PROGRAM = auto()
    WEB_SEARCH = auto()
    OPEN_WEBSITE = auto()
    UNKNOWN = auto()

@dataclass(frozen=True)
class Parsed:
    intent: Intent
    text: str

def normalize_ascii(s: str) -> str:
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii").lower().strip()

# ---- Helpers -----------------------------------

def _flatten_website_aliases() -> set[str]:
    aliases: set[str] = set()
    for k in WEBSITES.keys():
        if isinstance(k, (tuple, list)):
            for item in k:
                aliases.add(str(item).lower())
        else:
            aliases.add(str(k).lower())
    return aliases

_URL_LIKE_RE = re.compile(
    r"""^(
        https?:// |                    # scheme
        [a-z0-9.-]+\.[a-z]{2,} |       # domain.tld
        (localhost|\d{1,3}(\.\d{1,3}){3})(:\d+)? # localhost:3000 oder 127.0.0.1:8000
    )(/.*)?$""",
    re.IGNORECASE | re.VERBOSE,
)

def _is_url_like(token: str) -> bool:
    t = token.strip()
    return bool (_URL_LIKE_RE.match(t))

def _next_token_after_open(t: str) -> str:
    if not t.startswith("open"):
        return ""
    rest = t.split("open", 1)[1].strip()
    return rest.split()[0] if rest else ""

# ---- Main --------------------------------------

def parse_intent(task_lc: str) -> Parsed:
    t = normalize_ascii(task_lc)
    if not t:
        return Parsed(Intent.UNKNOWN, t)

    
    if matches_help(t):
        return Parsed(Intent.HELP, t)

    if matches_systeminfo(t):
        return Parsed(Intent.SYSTEMINFO, t)

    if any(k in t for k in ("time", "what time", "clock", "current time", "date", "today", "day")):
        return Parsed(Intent.TIME_OR_DATE, t)

    if t.startswith(("search for ", "search ", "google ")):
        return Parsed(Intent.WEB_SEARCH, t)

    
    if t.startswith("open "):
        token = _next_token_after_open(t)  
        if not token:
            return Parsed(Intent.UNKNOWN, t)

        prog_keys = set(PROGRAMME.keys())           
        web_aliases = _flatten_website_aliases()    

        if token in prog_keys:
            return Parsed(Intent.START_PROGRAM, t)

        
        if token in web_aliases or _is_url_like(token):
            return Parsed(Intent.OPEN_WEBSITE, t)

        
        for k in prog_keys:
            if k.startswith(token):
                return Parsed(Intent.START_PROGRAM, t)

        
        return Parsed(Intent.OPEN_WEBSITE, t)

    
    return Parsed(Intent.UNKNOWN, t)