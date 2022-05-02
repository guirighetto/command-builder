"""Module with run CI pipeline."""

from command_builder.command_builder import CommandBuilder


def main():
    """Run CI commands."""

    pipeline_builder = CommandBuilder()

    pipeline_builder.add(
        name="pytest",
        command=[
            "poetry",
            "run",
            "pytest",
            "--cov",
            "command_builder",
            "--cov-fail-under",
            "100",
            "--cov-report",
            "term-missing",
        ],
    )

    pipeline_builder.add(
        name="pylint",
        command=["poetry", "run", "pylint", "--fail-under", "10.0", "command_builder"],
    )

    pipeline_builder.add(
        name="black", command=["poetry", "run", "black", "--check", "--diff", "command_builder"]
    )

    pipeline_builder.add(name="mypy", command=["poetry", "run", "mypy", "-p", "command_builder"])

    pipeline_builder.run()
