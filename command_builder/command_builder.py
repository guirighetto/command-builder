"""Module containing the CommandBuilder for orchestrating shell command pipelines."""

import subprocess
from typing import List


class BColors:
    """ANSI escape sequences for coloured terminal output."""

    SUCCEEDED = "\033[92m"
    WARNING = "\033[93m"
    FAILED = "\033[91m"
    END = "\033[0m"


class CommandBuilder:
    """Orchestrates sequential execution of shell commands.

    When ``verbose=True`` (the default), all command output streams
    directly to the terminal — classic behaviour.

    When ``verbose=False``, stdout/stderr is captured and only a
    compact summary is printed, followed by the output of failed
    commands.  This is ideal for AI-agent consumers that need only
    pass/fail status without ingesting thousands of verbose lines.

    Args:
        verbose: If ``True``, stream command output to the terminal.
            If ``False``, capture output and print only the summary
            plus failed-command details.

    Example:
        Classic (verbose) behaviour::

            builder = CommandBuilder()
            builder.add("pytest", ["pytest"])
            builder.run()

        AI-friendly (summary-only) behaviour::

            builder = CommandBuilder(verbose=False)
            builder.add("pytest", ["pytest"])
            builder.run()
    """

    def __init__(self, verbose: bool = True) -> None:
        self.verbose = verbose
        self.commands: dict[str, dict] = {}

    def add(self, name: str, command: List[str]) -> None:
        """Register a command to be executed during :pymeth:`run`.

        Args:
            name: A short, human-readable label (e.g. ``"pytest"``).
            command: The command and its arguments as a list of strings.
        """
        self.commands[name] = {"command": command}

    def _print_summary(self) -> None:
        """Print a one-line-per-command pass/fail summary.

        When ``verbose=False``, also prints stdout/stderr of each
        failed command so the consumer knows *why* it failed without
        reading thousands of lines from passing tools.
        """
        print("_" * 30 + "summary" + "_" * 30)

        for name, command in self.commands.items():
            if command["returncode"] != 0:
                print(BColors.FAILED + f"ERROR: {name}: commands failed" + BColors.END)
                if not self.verbose:
                    self._print_failed_output(command)
            else:
                print(BColors.SUCCEEDED + f"{name}: commands succeeded" + BColors.END)

    @staticmethod
    def _print_failed_output(command: dict) -> None:
        """Print captured stdout/stderr of a failed command.

        Args:
            command: Internal command dict containing captured output.
        """
        stdout = command.get("stdout", "")
        stderr = command.get("stderr", "")
        if stdout:
            print(stdout)
        if stderr:
            print(stderr)

    def _run_command(self, command: List[str]) -> dict:
        """Execute a single command.

        Args:
            command: The command and its arguments as a list of strings.

        Returns:
            A dict with ``returncode`` and, when capturing, ``stdout``
            and ``stderr`` strings.
        """
        if self.verbose:
            run = subprocess.run(command, check=False, shell=False)
            return {"returncode": run.returncode}

        run = subprocess.run(
            command,
            check=False,
            shell=False,
            capture_output=True,
            text=True,
        )
        return {
            "returncode": run.returncode,
            "stdout": run.stdout,
            "stderr": run.stderr,
        }

    def run(self, summary: bool = True) -> None:
        """Execute all registered commands sequentially.

        Args:
            summary: If ``True``, print a compact pass/fail summary
                after execution.

        Raises:
            SystemExit: Always raised with the accumulated exit code
                so CI pipelines detect failures.
        """
        exit_code = 0

        for name, command in self.commands.items():
            result = self._run_command(command["command"])
            command.update(result)
            exit_code += result["returncode"]

        if summary:
            self._print_summary()

        raise SystemExit(exit_code)
