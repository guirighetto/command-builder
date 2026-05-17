"""Tests for the CommandBuilder."""
import pytest

from command_builder import CommandBuilder


def test_add(command_builder: CommandBuilder) -> None:
    """Test that ``add`` registers a command with the correct name and args."""
    command_builder.add("ls", ["ls", "--ilha"])

    assert command_builder.commands["ls"]["command"] == ["ls", "--ilha"]


def test_run_verbose_streams_output(
    command_builder: CommandBuilder,
    capfd: pytest.CaptureFixture,
) -> None:
    """Test verbose mode streams command output to the terminal."""
    command_builder.add("echo", ["echo", "hello"])

    with pytest.raises(SystemExit) as exc_info:
        command_builder.run(summary=False)

    assert exc_info.value.code == 0
    captured = capfd.readouterr()
    assert "hello" in captured.out


def test_run_quiet_captures_output(
    quiet_command_builder: CommandBuilder,
    capsys: pytest.CaptureFixture,
) -> None:
    """Test quiet mode captures output and does not show it in the terminal."""
    quiet_command_builder.add("echo", ["echo", "hello"])

    with pytest.raises(SystemExit) as exc_info:
        quiet_command_builder.run(summary=False)

    assert exc_info.value.code == 0
    captured = capsys.readouterr()
    assert "hello" not in captured.out
    assert captured.out == ""


def test_run_summary_shows_pass_fail(
    quiet_command_builder: CommandBuilder,
    capsys: pytest.CaptureFixture,
) -> None:
    """Test that the summary prints success and failure lines."""
    quiet_command_builder.add("success", ["echo", "hello"])
    quiet_command_builder.add("fail", ["false"])

    with pytest.raises(SystemExit) as exc_info:
        quiet_command_builder.run(summary=True)

    assert exc_info.value.code == 1
    captured = capsys.readouterr()
    assert "summary" in captured.out
    assert "success: commands succeeded" in captured.out
    assert "ERROR: fail: commands failed" in captured.out


def test_run_no_summary(
    quiet_command_builder: CommandBuilder,
    capsys: pytest.CaptureFixture,
) -> None:
    """Test that ``summary=False`` suppresses the summary block."""
    quiet_command_builder.add("echo", ["echo", "hello"])

    with pytest.raises(SystemExit) as exc_info:
        quiet_command_builder.run(summary=False)

    assert exc_info.value.code == 0
    captured = capsys.readouterr()
    assert "summary" not in captured.out


def test_run_quiet_prints_failed_output(
    quiet_command_builder: CommandBuilder,
    capsys: pytest.CaptureFixture,
) -> None:
    """Test that captured stdout/stderr of a failed command is printed inline."""
    quiet_command_builder.add("bad_ls", ["ls", "--invalid-flag-xyz"])

    with pytest.raises(SystemExit) as exc_info:
        quiet_command_builder.run(summary=True)

    assert exc_info.value.code != 0
    captured = capsys.readouterr()
    assert "ERROR: bad_ls: commands failed" in captured.out
    assert "invalid" in captured.out.lower()


def test_run_exit_code(command_builder: CommandBuilder) -> None:
    """Test that ``SystemExit`` carries the accumulated return code."""
    command_builder.add("ok", ["echo", "hello"])
    command_builder.add("nok", ["false"])

    with pytest.raises(SystemExit) as exc_info:
        command_builder.run(summary=False)

    assert exc_info.value.code == 1
