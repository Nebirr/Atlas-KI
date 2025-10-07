from __future__ import annotations
import os, json, sys, base64, hashlib, secrets
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional

APP_NAME = "Atlas"

def app_data_dir() -> Path:
    if sys.platform.startswith("win"):
        base = Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming"))
        return base / APP_NAME
    elif sys.platform == "darwin":
        return Path.home() / "Library" / "Application Support" / APP_NAME
    else:
        return Path.home() / ".config" / APP_NAME

def ensure_dirs() -> Path:
    d = app_data_dir()
    d.mkdir(parents=True, exist_ok=True)
    return d

# ------------- Password hashing (scrypt) -------------
def hash_password(password: str, salt: Optional[bytes] = None) -> dict:
    if salt is None:
        salt = secrets.token_bytes(16)
    pwd = password.encode("utf-8")
    key = hashlib.scrypt(pwd, salt=salt, n=2**14, r=8, p=1, dklen=32)
    return {
        "algo": "scrypt",
        # salt als HEX (wie bisher):
        "salt": base64.b16encode(salt).decode("ascii"),
        # hash als Base64 (wie bisher):
        "hash": base64.b64encode(key).decode("ascii"),
    }

def verify_password(password: str, record: dict) -> bool:
    try:
        # salt dekodieren (primär HEX, Fallback Base64)
        try:
            salt = base64.b16decode(record["salt"], casefold=True)
        except Exception:
            salt = base64.b64decode(record["salt"])

        # erwarteten Hash dekodieren (primär Base64, Fallback HEX)
        h = record["hash"]
        try:
            expect = base64.b64decode(h)
        except Exception:
            expect = base64.b16decode(h, casefold=True)

        # neu ableiten und vergleichen
        pwd = password.encode("utf-8")
        key = hashlib.scrypt(pwd, salt=salt, n=2**14, r=8, p=1, dklen=32)
        return secrets.compare_digest(key, expect)
    except Exception:
        return False

# ------------- Profiles -------------
PROFILES_FILE = "profiles.json"

def profiles_path() -> Path:
    return ensure_dirs() / PROFILES_FILE

def load_profiles() -> dict:
    p = profiles_path()
    if p.exists():
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            return {"users": {}}
    return {"users": {}}

def save_profiles(data: dict):
    profiles_path().write_text(json.dumps(data, indent=2), encoding="utf-8")

def create_user(username: str, password: str) -> bool:
    data = load_profiles()
    u = username.strip().lower()
    if not u or u in data["users"]:
        return False
    data["users"][u] = {
        "password": hash_password(password),
        "created": __import__("datetime").datetime.now().isoformat(timespec="seconds"),
        "roles": ["user"],
    }
    save_profiles(data)
    return True

def verify_user(username: str, password: str) -> bool:
    data = load_profiles()
    u = username.strip().lower()
    rec = data["users"].get(u)
    return verify_password(password, rec["password"]) if rec else False


def user_exists(username: str) -> bool:
    data = load_profiles()
    return username.strip().lower() in data["users"]

def set_user_password(username: str, new_password: str) -> bool:
    data = load_profiles()
    u = username.strip().lower()
    if u not in data["users"]:
        return False
    data["users"][u]["password"] = hash_password(new_password)
    save_profiles(data)
    return True

# ------------- Per-user settings -------------
@dataclass
class UserSettings:
    theme: str = "dark"
    font_family: str = "Segoe UI"
    font_size: int = 10
    window_width: int = 1200
    window_height: int = 800
    show_help_on_start: bool = False
    custom_aliases: dict | None = None

def settings_path(username: str) -> Path:
    u = username.strip().lower()
    return ensure_dirs() / f"settings_{u}.json"

def load_settings(username: str) -> UserSettings:
    p = settings_path(username)
    if p.exists():
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            return UserSettings(**{**UserSettings().__dict__, **data})
        except Exception:
            pass
    return UserSettings()

def save_settings(username: str, settings: UserSettings):
    p = settings_path(username)
    p.write_text(json.dumps(asdict(settings), indent=2), encoding="utf-8")