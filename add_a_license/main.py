# Add A License
#
# Description: The goal of this CLI application is for a user to be able to easily add
# various licenses to their project without having to cut and paste text.
#
# Workflow
# 1. aalicense with no input or --help should show what the program and commands do
# 2. aalicense GET <LICENSE> with no options should get the license and put it in the
#    current folder
# 3. aalicense GET <LICENSE> [DIRECTORY] should place the license in the given path
# 4. aalicense LIST should give and interactive prompt to choose either
#    A. from a list of top licenses OR B. A list of all licenses supported
# 5. After retrieving any license the cli should prompt for your <FULL NAME> to put in
#    the license
# 6. Ask if this a new project or not
# 7. (YES) just use the current year in the license file
# 8. (NO) Ask for year the project started and make year range with current year
# 9. If (NO) but input year is same is current year, notify that you will not use range
#    and just use current year

from pathlib import Path

import typer

from add_a_license.__version__ import __version__

app = typer.Typer()


def print_version():
    typer.echo(f"Add A License version: {__version__}")
    raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        False, "--version", "-v", help="Print version and exit.", callback=print_version
    )
):
    """
    A program to help you easily add a license to your project.
    """


@app.command("list")
def list_licenses():
    """
    Prompt user for what license they would like to add
    """
    pass


@app.command("get")
def get_license(
    license: str,
    dir: Path = typer.Option(
        ...,
        "--dir",
        "-d",
        exists=True,
        dir_okay=True,
        file_okay=False,
        writable=True,
        resolve_path=True,
    ),
):
    """
    Get a LICENSE file and copy it to the project
    """
    pass


if __name__ == "__main__":
    app()