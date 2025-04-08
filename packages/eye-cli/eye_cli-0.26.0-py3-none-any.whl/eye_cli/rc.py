import subprocess
import time
from pathlib import Path

import inquirer
import typer

from eye_cli.util import message, color, cmd, abort, find_bucket

app = typer.Typer(no_args_is_help=True)

RC = str(Path(r"C:\Program Files\Capturing Reality\RealityCapture\RealityCapture.exe"))


def start_rc(name):
    message(f"Starting Reality Capture ({name}) at {RC}")
    args = [RC, "-setInstanceName", name]
    subprocess.Popen(args)
    # TODO replace waiting with polling status
    time.sleep(5)


def delegate_to_rc(name, args):
    launch = [RC, "-delegateTo", name]
    launch.extend(args)
    message(f"Delegating to Reality Capture ({name}): {launch}")
    cmd(launch)


def rc_project(bucket, name):
    return Path(bucket) / "rc" / name / f"{name}.rcproj"


def get_local_rc_projects():
    """Get the local RC project names"""
    bucket = find_bucket(search_external_drives=False)
    rc_dir = Path(bucket) / "rc"
    if not rc_dir.is_dir():
        abort(f"No 'rc' dir in bucket. Should be here: {rc_dir}")
    rc_projects = [d for d in rc_dir.iterdir() if d.is_dir()]
    print(f"Found these RC proj dirs: ")
    for p in rc_projects:
        print(p)

    rc_projects = [p.name for p in rc_projects if (p / f"{p.name}.rcproj").is_file()]
    if not rc_projects:
        abort(f"There are no rc projects in {rc_dir}")
    return rc_projects


@app.command()
def simplify(
    project: str = "", component: str = "", relative_percent: int = 50, times: int = 1
):
    # TODO let me chose which project
    # TODO let me choose which component by querying after the project loads!
    message(color("Simplify", "yellow"), padding="around")

    # RC Executable
    if not Path(RC).is_file():
        abort(f"Could not find RC. Thought it was here: {RC}")

    # RC Project
    bucket = find_bucket()  # TODO add D drive
    if not project:
        project = inquirer.list_input("Which project?", choices=get_local_rc_projects())
    project_file = rc_project(bucket, project)
    if not project_file.is_file():
        abort(f"Thought i had a legit RC proj but this was not a file: {project_file}")

    instance = "RC1"
    start_rc(instance)

    # load project
    message(color("Loading Project: ", "green") + f" {project_file}...")
    # FIXME this fails. maybe the args are messed up.

    delegate_to_rc(instance, ["-load", str(project_file)])

    settings = [
        ("-selectComponent", component),
        # Means aim for a percentage of the current triangles
        ("-set", "mvsFltSimplificationType=1"),
        # target number of triangles in %
        ("-set", f"mvsFltTargetTrisCountRel={relative_percent}"),
        # this may be saying "leave any edges smaller than this" which could be very useful for keeping little details
        ("-set", "mvsFltMinEdgeLength=0.0"),
        # Simplify Border or no. 1 = Simplify ? = Keep
        ("-set", "mvsFltBorderDecimationStyle=1"),
        # affects density at part boundaries, select true for quality
        ("-set", "simplEqualizeDensity=true"),
        # when simplified parts get small, merge them? 2 = merge
        ("-set", "simplPreserveParts=2"),
        ### texture reprojection settings - not using
        # Reproject color? may reproject texture
        ("-set", "mvsFltReprojectColor=false"),
        # reproject normals into the new texture. no texture in this case
        ("-set", "mvsFltReprojectNormal=0"),
        # params for retexturing... not using these
        ("-set", "mvsFltUnwrapTexCount=0"),
        ("-set", "mvsFltUnwrapTexSide=0"),
    ]
    message(color("Setting Parameters", "green"))
    for s in settings:
        delegate_to_rc(instance, s)
    message(color("Saving", "green"))
    delegate_to_rc(instance, ["-save"])

    for i in range(1, times + 1):
        message(f"simplifying, iteration {i}/{times}")
        delegate_to_rc(instance, ["-simplify"])
        message(color("Saving", "green"))
        delegate_to_rc(instance, ["-save"])
