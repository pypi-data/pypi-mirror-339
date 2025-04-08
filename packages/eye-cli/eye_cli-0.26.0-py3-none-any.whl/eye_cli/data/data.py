import platform
import shlex
from itertools import islice
from pathlib import Path
from subprocess import CalledProcessError
from typing import Optional, List

import inquirer
import pyperclip
import typer
from typing_extensions import Annotated
from yaspin import yaspin
from yaspin.spinners import Spinners

from eye_cli.util import (
    message,
    color,
    cmd,
    abort,
    find_bucket,
    LOCAL,
    gs_path,
    commands,
    BUCKET,
)


def find_gsutil():
    system = platform.system()
    if system == "Windows":
        return str(
            Path(
                r"C:\Program Files (x86)\Google\Cloud SDK\google-cloud-sdk\bin\gsutil.cmd"
            )
        )
    else:
        return "gsutil"


GSUTIL = find_gsutil()

app = typer.Typer(no_args_is_help=True)


APP_NAME = "eye-cli"
CAPTURE = f"{BUCKET}/capture"
LOCAL_CAPTURE = LOCAL / "capture"


def ensure(p: Path):
    p.mkdir(parents=True, exist_ok=True)


@app.command()
def config():
    app_dir = typer.get_app_dir(APP_NAME)
    config_path: Path = Path(app_dir) / "config.json"
    if not config_path.is_file():
        message("No config present", padding="around")
    else:
        message("You have a config", padding="around")


@app.command()
def bucket(preview: bool = True, testing: bool = False):
    """Upload everything in your local bucket to the cloud"""
    m = color("UPLOAD", "red")
    message(f"{m} your whole bucket", padding="around")

    path = find_bucket(search_external_drives=True)

    message(f"{color("UPLOAD BUCKET", "red")} from {path}", padding="above")

    message("╮", indent=4)
    for i in Path(path).iterdir():
        message(f"├── {str(i.name)}", indent=4)
    message("╯", indent=4)

    to_path = (
        "gs://gecko-chase-photogrammetry-dev/testing/"
        if testing
        else "gs://gecko-chase-photogrammetry-dev/"
    )
    to_path = f'"{to_path}"'
    message(f"{color("TO", "red")} to {to_path}", padding="below")
    path = f'"{path}"'

    if not inquirer.confirm(
        "Are you sure you want to upload everything here?", default=False
    ):
        abort("")

    args = [GSUTIL, "-m", "rsync", "-r"]
    if preview:
        args.append("-n")
    args.extend([path, to_path])

    command = " ".join(args)
    message(f"{color("RUN THIS TO UPLOAD", "green")}  {command}", padding="above")
    message(
        f"{color(" └────> copied to your clipboard paste", "yellow")}", padding="below"
    )
    pyperclip.copy(command)


def get_local_captures():
    """Get the local Capture folders"""
    bucket = find_bucket(search_external_drives=True)
    capture_dir = Path(bucket) / "capture"
    if not capture_dir.is_dir():
        abort(f"No 'capture' dir in bucket. Should be here: {capture_dir}")
    captures = [d for d in capture_dir.iterdir() if d.is_dir()]
    if not captures:
        abort(f"There are no captures in {capture_dir}")
    return captures


def peek(path: Path):
    message("╮", indent=4)
    for i in islice(path.iterdir(), 10):
        message(f"├── {str(i.name)}", indent=4)
    message("╯", indent=4)


@app.command()
def capture(
    names: Annotated[Optional[List[str]], typer.Argument()] = None,
    preview: bool = True,
    raft: bool = False,
    run: bool = False,
):
    """Upload a capture folder to the cloud, or put it on a raft (external storage)."""
    # TODO implement --raft
    message(f"{color("UPLOAD", "red")} a capture folder", padding="around")

    if not names:
        paths = inquirer.checkbox("Which captures?", choices=get_local_captures())
        paths = [Path(p) for p in paths]
        names = [p.name for p in paths]
    else:
        bucket = find_bucket(search_external_drives=True)
        paths = [Path(bucket) / "capture" / n for n in names]

    for n, p in zip(names, paths):
        message(f"{color("UPLOAD", "red")} {n} {p}", padding="above")
        peek(p)

        to_path = f"gs://gecko-chase-photogrammetry-dev/capture/{n}"
        message(f"{color("TO", "red")} to {to_path}", padding="below")

    if not inquirer.confirm("Are you sure?", default=False):
        abort("by your request")

    message(f"{color("Run these commands to UPLOAD", "green")}", padding="above")
    to_paths = [gs_path("capture", n) for n in names]
    argss = [
        rsync_args(str(frm), to, preview=preview) for frm, to in zip(paths, to_paths)
    ]

    first_command = True
    for command in commands(argss):
        if first_command:
            first_command = False
            pyperclip.copy(command)
            extra_message = color(" ────> copied to your clipboard ", "yellow")
        else:
            extra_message = ""
        message(f"{command} {extra_message}", padding=None)

    if run:
        message(
            f"{color("NOTICE", "cyan")}: uploads run without progress indication. Watch your network activity.",
            padding="around",
        )
        for name, a in zip(names, argss):
            message(color("UPLOADING ", "red") + name)
            # TODO perhaps don't capture output- could be huge

            try:
                cmd(a)
            except CalledProcessError as e:
                if preview and e.returncode == 1:
                    pass
                else:
                    raise e

        message(color("UPLOADING COMPLETE", "green"), padding="around")


def rsync_args(
    frm: str,
    to: str,
    preview: bool = True,
) -> List[str]:
    args = [GSUTIL, "-m", "rsync", "-r"]
    if preview:
        args.append("-n")

    frm = quoted(frm)
    to = quoted(to)

    args.extend([frm, to])
    s = " ".join(args)
    args = shlex.split(s)
    return args


@app.command()
def down(name: str):
    m = color("DOWNLOAD", "green")
    message(f"{m} {name}", padding="around")

    from_path = f"{CAPTURE}/{name}"
    to = LOCAL_CAPTURE / name
    ensure(to)

    f = color(from_path, "blue")
    t = color(to, "orange")
    message(f"{m}\n{f} ->\n{t}", padding="around")

    cmd([GSUTIL, "-m", "rsync", "-r", from_path, to])


@app.command()
def folders(path=""):
    for r in get_cloud_folders(path=path):
        message(r, indent=4)


@yaspin(Spinners.aesthetic, text="Grabbing folders...", color="yellow")
def get_cloud_folders(path=""):
    """Get folders (not objects) in our bucket directly under the given path."""
    res = cmd([GSUTIL, "ls", f"{BUCKET}/{path}"])
    paths = res.stdout.split("\n")
    results = [p.split("/")[-2] for p in paths if p and p.split("/")[-1] == ""]
    results.sort(key=lambda s: s.lower())
    return results


# FIXME left off here listing local relevant folders
@yaspin(Spinners.aesthetic, text="Grabbing folders...", color="yellow")
def get_local_folders(path=""):
    """Get folders (not objects) in our bucket directly under the given path."""
    res = cmd([GSUTIL, "ls", f"{BUCKET}/{path}"])
    paths = res.stdout.split("\n")
    results = [p.split("/")[-2] for p in paths if p and p.split("/")[-1] == ""]
    results.sort(key=lambda s: s.lower())
    return results


if __name__ == "__main__":
    app()


def quoted(s: str) -> str:
    """Put quotes around the str"""
    return f'"{s}"'
