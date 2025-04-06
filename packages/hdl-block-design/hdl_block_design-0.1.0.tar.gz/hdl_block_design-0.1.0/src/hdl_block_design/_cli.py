"""Submodule defining the available CLI for this library."""

import importlib
import sys
from typing import Annotated

import typer

app = typer.Typer(invoke_without_command=True, no_args_is_help=True)


def print_package_version_and_exit() -> None:
    print(importlib.metadata.version(__package__.split(".")[0]))  # noqa: T201
    sys.exit(0)


@app.command()
def version() -> None:
    print_package_version_and_exit()


@app.command()
def other() -> None: ...


@app.callback()
def main(*, version: Annotated[bool, typer.Option("--version")] = False) -> None:
    if version:
        print_package_version_and_exit()
