#  SPDX-FileCopyrightText: 2025-present s-ball <s-ball@laposte.net>
#  #
#  SPDX-License-Identifier: MIT
import os
import sys
from typing import Any

from hatchling.builders.hooks.plugin.interface import BuildHookInterface

sys.path.append(os.path.dirname(__file__))
from hatch_pyside.build import build, clean

# A custom plugin to build the GUI
class CustomBuildHook(BuildHookInterface):

    def clean(self, _versions: list[str]) -> None:
        clean(os.path.join(self.root, 'src', 'hatch_pyside', 'gui'))

    def initialize(self, version: str, build_data: dict[str, Any]) -> None:
        build(os.path.join(self.root, 'src', 'hatch_pyside', 'gui'))
