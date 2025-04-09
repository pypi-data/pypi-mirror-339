"""Test the CLI module of Quine."""

import pytest

import quine.cli


def test_cli_output(capfd: pytest.CaptureFixture[str]) -> None:
    """
    Test CLI output of `main` function in `cli` module.

    :param capfd: pytest fixture to capture output.
    :return: None.
    """
    quine.cli.main()
    out, _ = capfd.readouterr()
    assert "Hello from Quine CLI!" in out
