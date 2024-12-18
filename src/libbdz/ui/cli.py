"""
Generate CLI based elements
"""

from rich import console
from rich import markdown

__console = console.Console()


def cinput(prompt: str) -> str:
    input_val = __console.input("[bold green]" + prompt + "[/]")
    return input_val


def cprint(message: str):
    __console.print(message, style="yellow")


def cprint_list(input: list[str]):
    print()
    for item in input:
        __console.print("    " + "\u2022 " + item, style="cyan")


def cprint_menu(menu_name: str, menu_list: list[str], menu_executables: list):
    while True:
        __console.print(
            "\n" + "    " + menu_name + "\n" + "    " + "=" * len(menu_name) + "\n",
            style="cyan",
        )

        count = 1
        for menu in menu_list:
            __console.print("    " + str(count) + ". " + menu, style="cyan")
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
    __console.print(md_content)
