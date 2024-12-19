"""
Generate CLI based elements
"""

from rich import console
from rich import live
from rich import spinner
from rich import table

_console = console.Console()


def cinput(prompt: str) -> str:
    input_val = _console.input("[bold green]" + prompt + "[/]")
    return input_val


def cprint(message: str):
    _console.print(message, style="yellow")


def cprint_menu(menu_name: str, menu_list: list[str], menu_executables: list):
    while True:
        _console.print(menu_name, style="cyan")
        for id, menu in enumerate(menu_list, start=1):
            _console.print(str(id) + ". " + menu, style="cyan")

        try:
            option = int(cinput("Enter your option (Ctrl-C to quit at any moment) : "))
        except KeyboardInterrupt:
            break
        except ValueError:
            cprint("Invalid option")
            continue

        if option > len(menu_list):
            cprint("Invalid option")
        else:
            try:
                menu_executables[option - 1]()
            except KeyboardInterrupt:
                cprint("Keyboard interrupt occured")


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

    _console.print(table_to_display)


class LiveStatusUpdate:
    def __init__(self, states: list[str]):
        self.__states = states
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
