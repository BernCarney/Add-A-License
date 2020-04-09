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
# 4. aalicense GET with no other input should give and interactive prompt to choose
#    either A. from a list of top licenses OR B. A list of all licenses supported
# 5. After retrieving any license the cli should prompt for your <FULL NAME> to put in
#    the license
# 6. Ask if this a new project or not
# 7. (YES) just use the current year in the license file
# 8. (NO) Ask for year the project started and make year range with current year
# 9. If (NO) but input year is same is current year, notify that you will not use range
#    and just use current year

import typer

app = typer.Typer()


@app.command()
def test123():
    """
    Test the CLI application
    """
    typer.echo("Testing that it works?")
