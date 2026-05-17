import pytest

from command_builder import CommandBuilder


@pytest.fixture
def command_builder() -> CommandBuilder:
    """Return a CommandBuilder with default verbose (terminal-streaming) settings."""
    return CommandBuilder()


@pytest.fixture
def quiet_command_builder() -> CommandBuilder:
    """Return a CommandBuilder with quiet (capture-only) settings."""
    return CommandBuilder(verbose=False)
