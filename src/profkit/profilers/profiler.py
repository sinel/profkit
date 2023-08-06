#  ********************************************************************************
#                        ______   _ __
#      ____  _________  / __/ /__(_) /_    Python toolkit
#     / __ \/ ___/ __ \/ /_/ //_/ / __/    for using profilers
#    / /_/ / /  / /_/ / __/ ,< / / /_      with support for
#   / .___/_/   \____/_/ /_/|_/_/\__/      filtering, analysis, and visualization
#  /_/
#
#  Copyright (c) 2023 Sinan Inel <sinan.inel@farsimple.com>
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#  ********************************************************************************
"""Profiler."""
from __future__ import annotations

from abc import abstractmethod
from typing import Any, Optional, Union

from loguru import logger


class Profiler:
    """Profiler class.

    Args:
        arg: ...
    """

    def __init__(self, arg: Optional[Any] = None):
        """Initialize Profiler."""
        self.arg = arg

    @abstractmethod
    def begin(self) -> Any:
        """Profiler.begin.

        Begin profiling.

        Returns:
            Any
        """

    @abstractmethod
    def end(self) -> Any:
        """Profiler.end.

        End profiling.

        Returns:
            Any
        """