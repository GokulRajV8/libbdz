"""
Generate number of files, total size and number of lines report
for every file type with exclusions
"""

import os
import re


def __prepare_pattern_matchers(exclude_patterns: list[str]) -> list[re.Pattern]:
    re_matchers = []
    for pattern in exclude_patterns:
        if pattern.startswith("#") or pattern == "\n":
            continue
        elif pattern.endswith("\n"):
            pattern = pattern[:-1]

        for character in [".", "^", "$", "+", "(", ")", "[", "]", "{", "}"]:
            pattern = pattern.replace(character, "\\" + character)

        if not pattern.startswith("/"):
            pattern = "*/" + pattern
        if pattern.endswith("/"):
            pattern = pattern + "*"
        re_matchers.append(re.compile(pattern.replace("*", "(.*?)")))

    return re_matchers


def __match_patterns(re_matchers: list[re.Pattern], input_str: str) -> bool:
    for re_matcher in re_matchers:
        result = re_matcher.fullmatch(input_str)
        if result is not None:
            return True
    return False


def __get_dir_entries(root: str, re_matchers: list[re.Pattern], dir: str = "/") -> list:
    abs_path = os.path.join(root, *dir.split("/"))
    result = [dir]

    for entry in os.listdir(abs_path):
        inner_entry = dir + entry
        if os.path.isfile(os.path.join(abs_path, entry)):
            if not __match_patterns(re_matchers, inner_entry):
                result.append(entry)
        else:
            if not __match_patterns(re_matchers, inner_entry + "/"):
                result.append(__get_dir_entries(root, re_matchers, inner_entry + "/"))

    return result


def __get_file_info(file: str):
    result = {}
    result["count"] = 1
    result["size"] = os.stat(file).st_size

    lines = 0
    with open(file, "r", encoding="utf-8") as fp:
        try:
            for line_number, _ in enumerate(fp):
                lines = line_number + 1
        except UnicodeDecodeError:
            pass
    result["lines"] = lines

    return result


def __process_dir_entries(root: str, dir_entries: list) -> dict:
    tld = dir_entries[0]
    abs_tld = os.path.join(root, *tld.split("/"))
    result = {}

    for idx in range(1, len(dir_entries)):
        entry = dir_entries[idx]
        if isinstance(entry, str):
            entry_arr = entry.split(".")
            key = "*" if len(entry_arr) == 1 else entry_arr[-1]
            file_data = {key: __get_file_info(os.path.join(abs_tld, entry))}
        else:
            file_data = __process_dir_entries(root, entry)

        for file_type in file_data:
            if file_type not in result:
                result[file_type] = {}
                result[file_type]["count"] = 0
                result[file_type]["size"] = 0
                result[file_type]["lines"] = 0

            result[file_type]["count"] += file_data[file_type]["count"]
            result[file_type]["size"] += file_data[file_type]["size"]
            result[file_type]["lines"] += file_data[file_type]["lines"]

    return result


def process(root: str, exclude_patterns_file: str) -> list[list[str]]:
    re_matchers = __prepare_pattern_matchers(exclude_patterns_file)
    dir_entries = __get_dir_entries(root, re_matchers)
    raw_data = __process_dir_entries(root, dir_entries)

    result = []
    for file_type in raw_data:
        count = str(raw_data[file_type]["count"])
        lines = str(raw_data[file_type]["lines"])
        orig_size = raw_data[file_type]["size"]
        if orig_size < 1024:
            size = str(orig_size) + " B"
        elif orig_size < 1024 * 1024:
            size = "%.2f" % (orig_size / 1024.0) + " KB"
        else:
            size = "%.2f" % (orig_size / (1024.0 * 1024.0)) + " MB"
        result.append([file_type, count, size, lines])
    result.sort(key=lambda x: x[0])

    return [["File type", "Count", "Total size", "Total lines"], *result]
