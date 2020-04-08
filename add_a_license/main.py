# Add A License
#
# Description: The goal of this CLI application is for a user to be able to easily add
# various licenses to their project without having to cut and paste text.
#

import typer

app = typer.Typer()


@app.command()
def test123():
    """
    Test the CLI application
    """
    typer.echo("Testing that it works?")
