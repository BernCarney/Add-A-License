from pathlib import Path
import datetime
import typer
import requests

from add_a_license.__version__ import __version__

# module variables
app = typer.Typer()
LICENSESAPI = "https://api.github.com/licenses"
NOW = datetime.datetime.now()
LICENSEFILE = "LICENSE"


def version_callback(value: bool):
    if value:
        typer.echo(f"Add A License version: {__version__}")
        raise typer.Exit()


# TODO Make this write licenses to a local cache so you don't always need to call API
def write_licenses(license_file):
    """
    Writes text to a license file
    """
    license_file.write("Some text written by the app")
    typer.echo("License written")


# TODO Make this read licenses from local cache if they exist instead of calling API
def read_licenses(license_file):
    """
    Reads text from a license file
    """
    for line in license_file:
        typer.echo(f"Config line: {line}")


# TODO Get license metadata (Permissions, Conditions, Limitations)
def get_metadata(license):
    """
    Gets metadata for a given LICENSE (Permissions, Conditions, Limitations)
    """
    pass


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


# TODO Extract common logic from get_license, list_licenses, and get_info to separate #      function to be more DRY
@app.command("get")
def get_license(
    license: str,
    full_name: str = typer.Option(
        ...,
        prompt="\nEnter your full name to be included in the LICENSE file",
        hidden=True,
    ),
    is_new: bool = typer.Option(True, prompt="\nIs this a new project?", hidden=True),
    dir: Path = typer.Option(
        "./",
        "--dir",
        "-d",
        dir_okay=True,
        file_okay=False,
        writable=True,
        resolve_path=True,
        help="Where you want the LICENSE file to be saved",
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
                # they selected a valid license, now get the license text
                license_json = requests.get(f"{LICENSESAPI}/{license.lower()}").json()
                license_bdy = license_json["body"]
                license_name = license_json["name"]

                # replace the [year] with current year
                if is_new:
                    license_bdy = license_bdy.replace("[year]", str(NOW.year), 1)
                else:
                    start_date = typer.prompt("What year did this project start?")
                    if start_date == str(NOW.year):
                        license_bdy = license_bdy.replace("[year]", str(NOW.year), 1)
                    else:
                        date_range = f"{start_date}-{str(NOW.year)}"
                        license_bdy = license_bdy.replace("[year]", date_range, 1)

                # replace [fullname] with prompted name
                license_bdy = license_bdy.replace("[fullname]", full_name, 1)

                # Check if directory exists and create if it doesn't
                path = Path(dir, LICENSEFILE)
                if not dir.exists():
                    dir.mkdir()
                # Write to LICENSE file
                typer.echo(f"\nWriting {license_name} to {path} file...")
                path.write_text(license_bdy)
                typer.echo("Finished!\n")

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
                # they selected a valid license, now get the license body
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
