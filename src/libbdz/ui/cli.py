"""
Generate CLI based elements
"""

from rich import console
from rich import live
from rich import spinner
from rich import table

_console = console.Console()


def _get_colored_text(text: str, color_code: int) -> str:
    color_key = ""
    match color_code:
        case 1:
            color_key = "[green]"
        case 2:
            color_key = "[yellow]"
        case 3:
            color_key = "[cyan]"
        case 4:
            color_key = "[red]"

    if color_key == "":
        return text
    else:
        return color_key + text + "[/]"


def _console_print(object_to_print, color_code: int = 0):
    _console.print()

    if isinstance(object_to_print, str):
        object_to_print = _get_colored_text(object_to_print, color_code)

    _console.print(object_to_print, highlight=False)


def cinput(prompt: str) -> str:
    input_val = _console.input(_get_colored_text("\n" + prompt, 1))
    return input_val


def cprint(message: str):
    _console_print(message, 2)


def cprint_menu(menu_name: str, menu_list: list[str], menu_executables: list):
    while True:
        _console_print(menu_name, 3)
        for id, menu in enumerate(menu_list, start=1):
            _console_print(str(id) + ". " + menu, 3)

        try:
            option = int(cinput("Enter your option (Ctrl-C to quit at any moment) : "))
        except KeyboardInterrupt:
            break
        except ValueError:
            _console_print("Invalid option", 2)
            continue

        if option > len(menu_list):
            _console_print("Invalid option", 2)
        else:
            try:
                menu_executables[option - 1]()
            except KeyboardInterrupt:
                _console_print("Keyboard interrupt occured", 2)


def cprint_table(
    title: str, headings: list[str], rows: list[list[str]], cell_alignment: list[str]
):
    column_count = len(headings)
    table_to_display = table.Table(title=title)
    for i in range(column_count):
        table_to_display.add_column(
            headings[i], justify="left" if cell_alignment[i] == "l" else "right"
        )

    for row in rows:
        table_to_display.add_row(*row)

    _console_print(table_to_display)


class LiveStatusUpdate:
    def __init__(self, states: list[str]):
        self.__states = [_get_colored_text(state, 4) for state in states]
        self.__count = 0
        self.__spinner = spinner.Spinner("dots", text=self.__states[self.__count])
        self.__live = live.Live(self.__spinner, console=_console, transient=True)
        self.__live.start()

    def update(self):
        self.__count += 1
        if self.__count < len(self.__states):
            self.__spinner.update(text=self.__states[self.__count])
            self.__live.update(renderable=self.__spinner)
        else:
            self.__live.stop()
