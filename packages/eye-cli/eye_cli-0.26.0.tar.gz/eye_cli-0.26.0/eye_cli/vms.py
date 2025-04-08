import subprocess

import inquirer
import typer
from rich import print
from rich.padding import Padding
from yaspin import yaspin
from yaspin.spinners import Spinners

from eye_cli.util import color, cmd

app = typer.Typer(no_args_is_help=True)


def message(s):
    print(Padding(s, 1))


@app.command()
def list():
    args = [
        "gcloud",
        "compute",
        "instances",
        "list",
        "--project",
        "fde-playground",
        "--format=table(name, zone, machineType, EXTERNAL_IP, status)",
        "--sort-by=name",
    ]
    for vm in get_vms(args):
        print(vm)


@app.command()
def running():
    args = [
        "gcloud",
        "compute",
        "instances",
        "list",
        "--project",
        "fde-playground",
        "--filter=status=RUNNING",
        "--format=table(name, zone, machineType, EXTERNAL_IP, status)",
        "--sort-by=name",
    ]
    for vm in get_vms(args):
        print(vm)


@app.command()
def start(keep_trying: bool = False, show_terminated: bool = False):

    message(f"{color("Which VMs should we start?", "blue")}")

    args = [
        "gcloud",
        "compute",
        "instances",
        "list",
        "--project",
        "fde-playground",
        "--format=table(name, status, zone, machineType)",
        "--sort-by=name",
    ]
    if not show_terminated:
        args.append("--filter=status=TERMINATED")

    vms = inquirer.checkbox("Which VMs?", choices=get_vms(args, header=False))

    # Get just name column
    vms = [vm.split()[0] for vm in vms]

    for vm in vms:
        uri = get_vm_uri(vm)

        try_again = True
        while try_again:
            message(f"{color("START", "green")} {vm}")
            try:
                start_vm(uri)
                try_again = False
            except (ValueError, subprocess.CalledProcessError):
                pass


def get_vms(args, header: bool = True):
    with yaspin(Spinners.aesthetic, text="Grabbing vms...", color="yellow") as spinner:
        res = cmd(args)
        vms = res.stdout.split("\n")
        vms = vms[:-1]
        if not header:
            vms = vms[1:]
        spinner.ok("✅ ")
        return vms


@app.command()
def stop(showall: bool = False):

    message(f"{color("Which VMs should we stop?", "blue")}")

    args = [
        "gcloud",
        "compute",
        "instances",
        "list",
        "--project",
        "fde-playground",
        "--format=table(name, status, zone, machineType)",
        "--sort-by=name",
    ]
    if not showall:
        args.append("--filter=status=RUNNING")

    vms = inquirer.checkbox("Which VMs?", choices=get_vms(args, header=False))

    # Get just name column
    vms = [vm.split()[0] for vm in vms]

    for vm in vms:
        message(f"{color("STOP", "red")} {vm}")
        try:
            uri = get_vm_uri(vm)
            stop_vm(uri)
        except (ValueError, subprocess.CalledProcessError):
            pass


def start_vm(uri):
    with yaspin(
        Spinners.aesthetic, text=f"Starting vm ({uri})...", color="yellow"
    ) as spinner:
        try:
            res = cmd(["gcloud", "compute", "instances", "start", uri])
            lines = res.stdout.split("\n")
            for l in lines:
                if "external IP" in l:
                    print(l)
            spinner.ok("✅ ")
        except subprocess.CalledProcessError as e:
            spinner.fail("💥 ")
            print(e.cmd)
            print(e.stderr)
            raise e


def stop_vm(uri):
    with yaspin(
        Spinners.aesthetic, text=f"Stopping vm ({uri})...", color="yellow"
    ) as spinner:
        try:
            cmd(["gcloud", "compute", "instances", "stop", uri])
            spinner.ok("✅ ")
        except subprocess.CalledProcessError as e:
            spinner.fail("💥 ")
            print(e.cmd)
            print(e.stderr)
            raise e


def get_vm_uri(name):
    with yaspin(
        Spinners.aesthetic, text=f"Getting URI for vm ({name})...", color="yellow"
    ) as spinner:
        try:
            res = cmd(
                [
                    "gcloud",
                    "compute",
                    "instances",
                    "list",
                    f"--filter=name:{name}",
                    "--uri",
                    "--project",
                    "fde-playground",
                ]
            )
            uri = res.stdout.split("\n")[0]
            if uri:
                spinner.ok("✅ ")
                return uri
            else:
                raise ValueError(f"Couldn't get URI for vm {name}")
        except (ValueError, subprocess.CalledProcessError) as e:
            spinner.fail("💥 ")
            raise e


if __name__ == "__main__":
    app()
