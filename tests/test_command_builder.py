"""Module for testinig the CommandBuilder."""

import pytest


def test_add(command_builder):
    """Test the add method."""
    command_builder.add("ls", ["ls", "--ilha"])

    assert command_builder.commands["ls"]["command"] == ["ls", "--ilha"]


def test_run(command_builder):
    """Test the run method."""

    command_builder.add("ls", ["ls", "-ilha"])
    command_builder.add("pwd", ["pwd", "-o"])

    command_builder.run()

    assert command_builder.commands["ls"]["returncode"] == 0
    assert command_builder.commands["pwd"]["returncode"] != 0
