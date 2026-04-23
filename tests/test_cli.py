from typer.testing import CliRunner

from app.cli import app


def test_cli_help_lists_commands():
	runner = CliRunner()
	result = runner.invoke(app, ["--help"])

	assert result.exit_code == 0
	assert "sync" in result.output
	assert "eval" in result.output
