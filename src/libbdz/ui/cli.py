"""
Generate CLI based elements
"""

from rich import console
from rich import live
from rich import markdown
from rich import spinner

_console = console.Console()


def cinput(prompt: str) -> str:
    input_val = _console.input("[bold green]" + prompt + "[/]")
    return input_val


def cprint(message: str):
    _console.print(message, style="yellow")


def cprint_list(input: list[str]):
    print()
    for item in input:
        _console.print("    " + "\u2022 " + item, style="cyan")


def cprint_menu(menu_name: str, menu_list: list[str], menu_executables: list):
    while True:
        _console.print(
            "\n" + "    " + menu_name + "\n" + "    " + "=" * len(menu_name) + "\n",
            style="cyan",
        )

        count = 1
        for menu in menu_list:
            _console.print("    " + str(count) + ". " + menu, style="cyan")
            count += 1

        try:
            option = int(cinput("Enter your option (Ctrl-C to quit at any moment) : "))
        except KeyboardInterrupt:
            print()
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
                print()
                cprint("Keyboard interrupt occured")


def cprint_md(content: str):
    md_content = markdown.Markdown(content)
    _console.print(md_content)


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
