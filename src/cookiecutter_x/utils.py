import logging
import os
import stat
import sys
from typing import List, Tuple, Union

from tabulate import tabulate


def print_table(table: List[List[str]], headers: List[str], stderr: bool = False) -> None:
    print_file = sys.stderr if stderr else sys.stdout
    print(tabulate(table, headers=headers, tablefmt="pipe", numalign="right"), file=print_file)


def gen_banner(s: str, level: int) -> str:
    return f"{'#' * level} {s}{os.linesep}"


def make_file_executable(file_path: str) -> None:
    if not os.path.exists(file_path):
        logging.warning(f"File not found {file_path}; doing nothing.")
        return

    logging.info(f"Making file executable: {file_path}")
    st = os.stat(file_path)
    os.chmod(file_path, st.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def format_sections(sections: List[Tuple[str, Union[str, List[str]]]]) -> str:
    msg = ''
    for header, content in sections:
        if isinstance(content, list):
            c = "- " + f"{os.linesep}- ".join(content)
        else:
            c = content

        msg += os.linesep + header + os.linesep \
               + len(header) * '-' + os.linesep \
               + c.rstrip() + os.linesep

    return msg


def make_dirs(path: str) -> None:
    if not os.path.exists(path):
        logging.info(f"Creating {path}")
        os.makedirs(path)


def write_content(file_name: str, content: str) -> None:
    logging.info(f"Writing {file_name}")
    with open(file_name, 'w') as f:
        f.write(content)
