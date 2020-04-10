from typer.testing import CliRunner

from add_a_license.main import app

runner = CliRunner()


def test_add_a_license():
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "Add A License version: 0.1.0\n" in result.stdout
