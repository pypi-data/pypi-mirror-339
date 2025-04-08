import shlex

import inquirer
import typer

from eye_cli.util import color, message

app = typer.Typer(no_args_is_help=True)


@app.command()
def split():
    line = inquirer.text(message="Enter your command line input")
    args = shlex.split(line)
    message(color("ARGS: ", "blue") + f"{args}", padding="above")
    message(color("FLIP:  ", "blue") + shlex.join(args), padding="below")
