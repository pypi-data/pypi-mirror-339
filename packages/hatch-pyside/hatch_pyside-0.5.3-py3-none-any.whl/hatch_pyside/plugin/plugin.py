#  SPDX-FileCopyrightText: 2025-present s-ball <s-ball@laposte.net>
#  #
#  SPDX-License-Identifier: MIT
import os
from typing import Any

from hatchling.builders.hooks.plugin.interface import BuildHookInterface
from ..build import build, clean

class PysideBuildHook(BuildHookInterface):
    PLUGIN_NAME = 'pyside'

    def clean(self, _versions: list[str]) -> None:
        for f in self.config['folders']:
            clean(os.path.join(self.root, f))

    def initialize(self, version: str, build_data: dict[str, Any]) -> None:
        for f in self.config['folders']:
            build(os.path.join(self.root, f))
        build_data['artifacts'].append('ui_*.py')