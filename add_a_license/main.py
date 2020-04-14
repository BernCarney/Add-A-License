# Add A License
#
# Description: The goal of this CLI application is for a user to be able to easily add
# various licenses to their project without having to cut and paste text.
#
# Workflow
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
import datetime
import typer
import requests

from add_a_license.__version__ import __version__

# module variables
app = typer.Typer()
LICENSESAPI = "https://api.github.com/licenses"
NOW = datetime.datetime.now()


def version_callback(value: bool):
    if value:
        typer.echo(f"Add A License version: {__version__}")
        raise typer.Exit()


def write_licenses(license_file):
    """
    Writes text to a license file
    """
    license_file.write("Some text written by the app")
    typer.echo("License written")


def read_licenses(license_file):
    """
    Reads text from a license file
    """
    for line in license_file:
        typer.echo(f"Config line: {line}")


@app.callback()
def main(
    version: bool = typer.Option(
        None,
        "--version",
        "-v",
        help="Print version and exit.",
        callback=version_callback,
        is_eager=True,
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
    try:
        r = requests.get(LICENSESAPI)
        licenses_json = r.json()

        if r.status_code == 200:
            typer.echo("Available licenses:\n")
            i = 1
            for item in licenses_json:
                name = item["name"]
                abbr = item["spdx_id"]
                typer.echo(f"{i:02d}. {abbr}:  {name}")
                i += 1
    except requests.exceptions.Timeout:
        # prompt to retry connection
        pass


@app.command("get")
def get_license(
    license: str,
    dir: Path = typer.Option(
        "./",
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
    try:
        r = requests.get(LICENSESAPI)
        licenses_json = r.json()
        licenses_lst = []

        # make sure API is available
        if r.status_code == 200:
            # build a list of the licenses available
            for item in licenses_json:
                licenses_lst.append(item["key"])

            if license.lower() in licenses_lst:
                # they selected a valid license, now get the test
                license_json = requests.get(f"{LICENSESAPI}/{license.lower()}").json()
                license_bdy = license_json["body"]

                # replace the [year] woth current year
                license_bdy = license_bdy.replace("[year]", str(NOW.year), 1)
                license_bdy = license_bdy.replace("[fullname]", "Bernard J. Carney", 1)
                typer.echo(f"{license_bdy}")
            else:
                typer.echo("That license is not currently available.")
                typer.echo("Please choose a license from available licenses below:\n")
                i = 1
                for item in licenses_json:
                    name = item["name"]
                    abbr = item["spdx_id"]
                    typer.echo(f"{i:02d}. {abbr}:  {name}")
                    i += 1
        else:
            typer.echo(f"We didn't do it unfortunately")
    except requests.exceptions.Timeout:
        # prompt to retry connection
        pass


@app.command("info")
def get_info(license: str):
    """
    Get a LICENSE info and print to terminal.
    """

    try:
        r = requests.get(LICENSESAPI)
        licenses_json = r.json()
        licenses_lst = []

        # make sure API is available
        if r.status_code == 200:
            # build a list of the licenses available
            for item in licenses_json:
                licenses_lst.append(item["key"])

            if license.lower() in licenses_lst:
                # they selected a valid license, now get the test
                license_json = requests.get(f"{LICENSESAPI}/{license.lower()}").json()
                license_dsc = license_json["description"]
                license_name = license_json["name"]
                license_url = license_json["html_url"]
                license_perm = []

                for item in license_json["permissions"]:
                    license_perm.append(item)

                typer.echo(f"\nName: {license_name}")
                typer.echo(f"\nURL: {license_url}")

                # print list of permissions
                typer.echo(f"\nPermissions:")
                for x in license_perm:
                    typer.echo(f"\t{x}")
                typer.echo(f"\nDescription: \n\t{license_dsc}\n")
            else:
                typer.echo("That license is not currently available.")
                typer.echo("Please choose a license from available licenses below:\n")
                i = 1
                for item in licenses_json:
                    name = item["name"]
                    abbr = item["spdx_id"]
                    typer.echo(f"{i:02d}. {abbr}:  {name}")
                    i += 1
        else:
            typer.echo(f"We didn't do it unfortunately")
    except requests.exceptions.Timeout:
        # prompt to retry connection
        pass


if __name__ == "__main__":
    app()
