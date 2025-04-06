#  SPDX-FileCopyrightText: 2025-present s-ball <s-ball@laposte.net>
#  #
#  SPDX-License-Identifier: MIT
"""This module wraps the calls to the pyside6-project command
used to build the relevant .py file from the Qt source ones
or to remove them.

command contains the full path of the first found pyside-project command.
"""
import os
import shutil
import subprocess
import sysconfig

__all__ = ["command", "build", "clean"]

from subprocess import CalledProcessError

from typing import Any

from hatchling.builders.hooks.plugin.interface import BuildHookInterface

command: list[str]


def run(cmd, folder) -> None:
    """
    Pass the subcommand cmd to pyside6-project with the folder parameter
    Args:
        cmd:    the subcommand to execute (should be clean or build)
        folder: the folder containing the .pyproject file

    Raises:
        CalledProcessError  if the pyside6-project command returns a non 0 exit code
    """
    subprocess.run(
        command + [cmd, folder],
        stdin=subprocess.DEVNULL,
        capture_output=True,
        text=True,
        check=True,
        creationflags=subprocess.CREATE_NO_WINDOW,
    )


def build(folder: str) -> None:
    """
    Calls run to build the dependant files
    Args:
        folder:  the folder containing the .pyproject file

    Raises:
        CalledProcessError  if the pyside6-project command returns a non 0 exit code
    """
    run("build", folder)


def clean(folder: str) -> None:
    """
    Calls run to clean the dependant files
    Args:
        folder:  the folder containing the .pyproject file

    Raises:
        CalledProcessError  if the pyside6-project command returns a non 0 exit code
    """
    run("clean", folder)


def _build_command() -> str:
    # first search the command in the path
    prog = "pyside6-project"
    cmd = shutil.which(prog)
    if cmd is None:
        # else search it in any possible script installation folder
        visited = set()
        for d in (
            sysconfig.get_path("scripts", scheme)
            for scheme in sysconfig.get_scheme_names()
        ):
            if d in visited:  # only search once in each folder
                continue
            visited.add(d)
            cmd = shutil.which(prog)
            if cmd is not None:
                break
        else:
            raise RuntimeError(f"No installation of {prog} found")
    return cmd


# compute command at import time
command = [_build_command()]

# A custom plugin to build the GUI
class CustomBuildHook(BuildHookInterface):

    def clean(self, _versions: list[str]) -> None:
        clean(os.path.join(self.root, 'src', 'hatch_pyside', 'gui'))

    def initialize(self, version: str, build_data: dict[str, Any]) -> None:
        os.listdir()
        self.app.display_info(f"Custom plugin in {self.root}: {str(os.listdir(self.root))}")
        self.app.display_info(f"{str(os.listdir(os.path.join(self.root, 'src', 'hatch_pyside', 'gui')))}")
        try:
            build(os.path.join(self.root, 'src', 'hatch_pyside', 'gui'))
        except subprocess.CalledProcessError as e:
            self.app.display_error(f'Command {e.cmd} returned {e.returncode}\n'
                                   f'stdout: {e.stdout}\n'
                                   f'stderr: {e.stderr}\n')
            raise
