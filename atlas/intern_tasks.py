import os
import platform, psutil, GPUtil
from tabulate import tabulate
from datetime import datetime
from atlas.lists import PROGRAMME 
import unicodedata


SYSTEMINFO_KEYWORDS = ["systeminfo", "system information", "pc info", "hardware"]

def normalize_ascii(s: str) -> str:
    
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii").lower().strip()

def matches_systeminfo(task_lc: str) -> bool:
    t = normalize_ascii(task_lc)
    return any(k in task_lc for k in SYSTEMINFO_KEYWORDS)

def collect_system_info_rows() -> list[tuple[str, str]]:
    
    rows: list[tuple[str, str]] = [
        ("OS", f"{platform.system()} {platform.release()}"),
        ("Version", platform.version()),
        ("CPU", platform.processor()),
        ("RAM", f"{round(psutil.virtual_memory().total / (1024**3), 2)} GB"),
    ]
    
    try:
        gpus = GPUtil.getGPUs()
        if gpus:
            for i, gpu in enumerate(gpus):
                rows.append((f"GPU {i}", f"{gpu.name} ({round(gpu.memoryTotal/1024, 2)} GB VRAM)"))
        else:
            rows.append(("GPU", "No GPU detected"))
    except Exception as e:
        rows.append(("GPU", f"Error: {e}"))
    return rows

def render_system_info() -> str:
    
    infos = collect_system_info_rows()
    return "\n".join([
        "=== System Information ===",
        tabulate(infos, headers=["Category", "Value"], tablefmt="fancy_grid")
    ])

def show_system_info() -> None:
    print(render_system_info())

def start_programm(task_lc: str) -> bool:
    """
    English trigger: 'open <name>'.
    Keeps function name for backward compatibility.
    """
    t = normalize_ascii(task_lc)
    if not t.startswith("open "):
        return False
    try:
        target_key = t.split("open", 1)[1].strip().split()[0]
    except IndexError:
        print("Please specify what to open (e.g., 'open downloads')."); return True
    if target_key in PROGRAMME:
        os.startfile(PROGRAMME[target_key])
        print(f"{target_key.capitalize()} is being opened.")
        return True
    print(f"Unknown program/folder '{target_key}'. Type 'help' to see available names.")
    return True  

def handle_time_or_date(task_lc: str) -> bool:
    t = normalize_ascii(task_lc)
    if any(k in t for k in ["time", "what time", "clock", "current time"]):
        print("It is currently", datetime.now().strftime("%H:%M:%S"))
        return True
    if any(k in t for k in ["date", "today", "day"]):
        print("Today is", datetime.now().strftime("%Y-%m-%d"))
        return True
    return False