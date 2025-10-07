from tabulate import tabulate
from atlas.lists import WEBSITES, PROGRAMME

COMMANDS = [
    {"Category": "System", "Command": "help", "Description": "Show this help", "Example": "help"},
    {"Category": "System", "Command": "exit", "Description": "Quit the assistant", "Example": "exit"},
    {"Category": "Info",   "Command": "systeminfo", "Description": "Show system information", "Example": "systeminfo"},
    {"Category": "Time",   "Command": "time", "Description": "Show current time", "Example": "what time is it"},
    {"Category": "Time",   "Command": "date", "Description": "Show today's date", "Example": "what's the date"},
    {"Category": "Apps",   "Command": "open <name>", "Description": "Open a program or folder", "Example": "open downloads"},
    {"Category": "Web",    "Command": "open <alias|url>", "Description": "Open a website", "Example": "open yt"},
    {"Category": "Web",    "Command": "search for <query>", "Description": "Google search", "Example": "search for python lists"},
]

HELP_KEYWORDS = ["help", "commands", "command list", "?"]


def matches_help(task_lc: str) -> bool:
    return any(k in task_lc for k in HELP_KEYWORDS)


def render_help() -> str:
    rows = [[c["Category"], c["Command"], c["Description"], c["Example"]] for c in COMMANDS]
    parts: list[str] = []
    parts.append("=== Command Overview ===")
    parts.append(tabulate(rows, headers=["Category","Command","Description","Example"], tablefmt="fancy_grid"))

    web_rows = [[", ".join(keys), url] for keys, url in WEBSITES.items()]
    if web_rows:
        parts.append("\n-- Website-Aliasse (WEBSITES) --")
        parts.append(tabulate(web_rows, headers=["Alias(es)","URL"], tablefmt="fancy_grid"))

    prog_rows = [[name, str(target)] for name, target in PROGRAMME.items()]
    if prog_rows:
        parts.append("\n-- Programs/Folders (PROGRAMME) --")
        parts.append(tabulate(prog_rows, headers=["Name","Target"], tablefmt="fancy_grid"))

    return "\n".join(parts)

def show_help() -> None:
    print(render_help())