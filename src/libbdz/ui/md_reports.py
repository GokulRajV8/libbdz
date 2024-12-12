"""
Generate reports in markdown format
"""


def generate_table(
    headings: list[str], rows: list[list[str]], cell_alignment: list[str]
) -> str:
    result = ""
    for heading in headings:
        result += "| " + heading + " "
    result += "|\n"

    for entry in cell_alignment:
        if entry == "l":
            alignment = ":--"
        elif entry == "r":
            alignment = "--:"
        else:
            alignment = ":-:"
        result += "| " + alignment + " "
    result += "|\n"

    for row in rows:
        for cell in row:
            result += "| " + cell + " "
        result += "|\n"

    return result
