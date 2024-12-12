"""
Generate CLI based elements
"""


def __get_colored_string(input: str, color_code: int) -> str:
    match color_code:
        case 1:
            return f"\033[92m{input}\033[0m"
        case 2:
            return f"\033[93m{input}\033[0m"
        case 3:
            return f"\033[96m{input}\033[0m"
        case _:
            return input


def cprint(message: str):
    print("\n" + __get_colored_string(message, 2))


def cprint_list(input: list[str]):
    print()
    for item in input:
        print("    " + "\u2022 " + __get_colored_string(item, 3))


def cinput(prompt: str) -> str:
    return input("\n" + __get_colored_string(prompt, 1))
