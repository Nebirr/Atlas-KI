from __future__ import annotations
import io
from contextlib import redirect_stdout

from atlas.core.intent import parse_intent, Intent

from atlas.extern_tasks import handle_search, open_website

from atlas.help_cmd import render_help
from atlas.intern_tasks import (
    handle_time_or_date,
    render_system_info,
    start_programm,
)


class AtlasService: 
    def process_command(self, text: str) -> str:
        task_lc = (text or "").strip()
        if not task_lc:
            return ""

        parsed = parse_intent(task_lc)

        buf = io.StringIO()
        with redirect_stdout(buf):
            match parsed.intent:
                
                case Intent.HELP:
                    return render_help()

                case Intent.TIME_OR_DATE:
                    handle_time_or_date(task_lc)
                    return buf.getvalue().strip()

                case Intent.START_PROGRAM:
                    start_programm(task_lc)
                    return buf.getvalue().strip()

                case Intent.SYSTEMINFO:
                    return render_system_info()

                case Intent.WEB_SEARCH:
                    handle_search(task_lc)
                    return buf.getvalue().strip()

                case Intent.OPEN_WEBSITE:
                    open_website(task_lc)
                    return buf.getvalue().strip()
                
                case Intent.UNKNOWN:
                    print("Dont know this Task, type 'help' for advice.")
                    return buf.getvalue().strip()