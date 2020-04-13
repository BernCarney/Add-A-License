from typer.testing import CliRunner

from add_a_license.main import app

runner = CliRunner()


def test_version():
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "Add A License version: 0.1.0\n" in result.stdout


def test_no_input_help():
    result = runner.invoke(app)
    assert result.exit_code == 0
    assert "Usage: main [OPTIONS] COMMAND [ARGS]...\n\n" in result.stdout


def test_list_licenses():
    result = runner.invoke(app, ["get", "MIT"])
    assert result.exit_code == 0
    pass


def test_get_license():
    pass


def test_get_nan_license():
    pass


def test_invalid_option():
    pass


def test_invalid_command():
    pass
