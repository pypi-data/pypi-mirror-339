import subprocess
from pathlib import Path
from typing import List

import inquirer
import typer
from rich import print
from rich.padding import Padding


def abort(s):
    header = color("Exiting... ", "red")
    message(header + s, padding="around")
    raise typer.Abort()


def message(the_message, padding=None, indent: int = 0):
    if indent:
        the_message = Padding.indent(the_message, indent)

    if padding == "around":
        the_message = Padding(the_message, pad=(1, 2, 1, 2))
    elif padding == "above":
        the_message = Padding(the_message, pad=(1, 2, 0, 2))
    elif padding == "below":
        the_message = Padding(the_message, pad=(0, 2, 1, 2))

    print(the_message)


def color(s, color):
    return f"[bold {color}]{s}[/]"


def cmd(args):
    return subprocess.run(args, check=True, capture_output=True, encoding="utf-8")


def find_bucket(search_external_drives: bool = False) -> str:
    """Return its path"""
    paths = []

    # search on attached drives
    if search_external_drives:
        attached = [d / "bucket" for d in Path("/Volumes").iterdir()]
        paths.extend(attached)

    # search on local machine
    paths.append(LOCAL)
    paths.append(Path(r"D:\bucket"))

    # narrow to those that are present
    paths = [d for d in paths if d.is_dir()]

    paths = [str(p) for p in paths]
    if not paths:
        abort("Can't find your bucket, where is it?")
    if len(paths) == 1:
        path = paths[0]
    else:
        path = inquirer.list_input("Which bucket?", choices=paths)

    return path


LOCAL = Path.home() / "Downloads" / "bucket"

BUCKET = "gs://gecko-chase-photogrammetry-dev"


def gs_path(kind: str, name: str, bucket: str = BUCKET):
    return f"{bucket}/{kind}/{name}"


def commands(argss: List[List[str]]) -> List[str]:
    """Given a list of, a list of command line args,
    stringify the args appropriate for typing into the command line, and return each
    """
    return [" ".join(args) for args in argss]
