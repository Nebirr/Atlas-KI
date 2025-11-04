# main.py
from atlas.core.intent import parse_intent, Intent
from atlas.help_cmd import show_help
from atlas.intern_tasks import show_system_info, handle_time_or_date, start_programm
from atlas.extern_tasks import handle_search, open_website
from atlas.atlas_gui.speech_widget import SpeechWidget

while True:
    task = input("Frag mich etwas ...: ")
    task_lc = task.lower().strip()

    if task_lc == "exit":
        print("Okay, bis bald!"); break

    parsed = parse_intent(task_lc)

    match parsed.intent:
        case Intent.HELP:
            show_help()

        case Intent.SYSTEMINFO:
            show_system_info()

        case Intent.TIME_OR_DATE:
            handle_time_or_date(task_lc)

        case Intent.START_PROGRAM:
            start_programm(task_lc)

        case Intent.WEB_SEARCH:
            handle_search(task_lc)

        case Intent.OPEN_WEBSITE:
            open_website(task_lc)

        case Intent.UNKNOWN:
            print("Dont know this Task, type 'help' for advice.")
