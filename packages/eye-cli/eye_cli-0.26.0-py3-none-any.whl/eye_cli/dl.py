from enum import Enum
from pathlib import Path
from subprocess import CalledProcessError
from typing import Annotated, Optional, List

import inquirer
import pyperclip
import typer

from .data.data import get_cloud_folders, rsync_args
from .util import (
    find_bucket,
    gs_path,
    message,
    color,
    commands,
    cmd,
)

cli = typer.Typer(no_args_is_help=True)


def local_path(kind: str, name: str, bucket: str) -> Path:
    return Path(bucket) / kind / name


class DataKind(Enum):
    capture = "capture"
    rc = "rc"
    rc_export = "rc-export"
    alignedLaser = "alignedLaser"


class DataMovementWay(Enum):
    down = "down"
    up = "up"


@cli.callback()
def callback():
    pass


@cli.command()
def move(
    kind: Annotated[Optional[DataKind], typer.Option()] = None,
    names: Annotated[Optional[List[str]], typer.Argument()] = None,
    way: Annotated[Optional[DataMovementWay], typer.Option()] = None,
    preview: bool = True,
    run: bool = False,
):
    if not way:
        way = inquirer.list_input(
            "Upload or Download?", choices=[e.value for e in DataMovementWay]
        )

    if not kind:
        kind = inquirer.list_input("Which kind?", choices=[e.value for e in DataKind])

    if not names:
        if way == DataMovementWay.down:
            names = inquirer.checkbox(
                f"Which {kind}s?", choices=get_cloud_folders(path=kind)
            )
        else:
            names = inquirer.checkbox(
                f"Which {kind}s?", choices=get_local_folders(path=kind)
            )
    bucket = find_bucket()

    argss = []
    for n in names:
        frm = gs_path(kind, n)
        to = local_path(kind, n, bucket)
        to.mkdir(exist_ok=True, parents=True)  # TODO possibly confirm before doing this
        args = rsync_args(frm, str(to), preview=preview)
        argss.append(args)
        message(f"{color("DOWNLOAD", "blue")} {n} {frm}", padding="above")
        message(f"{color("TO", "blue")} to {str(to)}", padding="below")

    message(f"{color("Run these commands to DOWNLOAD", "green")}", padding="above")
    first_command = True
    for command in commands(argss):
        if first_command:
            first_command = False
            pyperclip.copy(command)
            extra_message = color(" ────> copied to your clipboard ", "yellow")
        else:
            extra_message = ""
        message(f"{command} {extra_message}", padding=None)

    # run the commands
    if run:
        message(
            f"{color("NOTICE", "cyan")}: uploads run without progress indication. Watch your network activity.",
            padding="around",
        )
        for name, args in zip(names, argss):
            message(color("DOWNLOADING ", "blue") + name)
            # TODO perhaps don't capture output- could be huge

            try:
                cmd(args)
            except CalledProcessError as e:
                if preview and e.returncode == 1:
                    # FIXME this should error out because the directory doesn't exist - but currently doesnt
                    # 1 is the return code for success when you run rsync in preview
                    pass
                else:
                    raise e

        message(color("DOWNLOADS COMPLETE", "green"), padding="around")
