import pytest

from command_builder import CommandBuilder


@pytest.fixture(scope="function")
def command_builder() -> CommandBuilder:
    """Fixture that returns the CommandBuilder."""

    return CommandBuilder()
