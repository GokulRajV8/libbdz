"""
Organize files in device
"""

import os
import shutil


def __move_file_with_rename(file_name: str, file_type: str, src_dir: str, dst_dir: str):
    count = 0
    final_file_name = file_name
    final_file_type = "" if file_type == "*" else "." + file_type
    while True:
        if os.path.isfile(os.path.join(dst_dir, final_file_name + final_file_type)):
            count += 1
            final_file_name = file_name + "-" + str(count)
        else:
            shutil.move(
                os.path.join(src_dir, file_name + final_file_type),
                os.path.join(dst_dir, final_file_name + final_file_type),
            )
            break


def move_particular_filetypes(src: str, dst: str, file_types: list[str]):
    """
    Moves files from src to dst directories.
    If file already present in dst directory, the file name is appended with "-count"
    """
    for file in os.listdir(src):
        abs_file = os.path.join(src, file)
        if os.path.isfile(abs_file):
            file_name_arr = file.split(".")
            if len(file_name_arr) == 1:
                file_name, file_type = file_name_arr[0], "*"
            else:
                file_name, file_type = ".".join(file_name_arr[:-1]), file_name_arr[-1]
            if file_type.lower() in file_types:
                __move_file_with_rename(file_name, file_type, src, dst)
