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
from enum import StrEnum
from typing import Any, Optional

from profkit.settings import ProfilerSettings


class Profiler:
    """Profiler class.

    Args:
        settings: Profiler settings.
    """

    class OutputType(StrEnum):
        """Export type enumeration."""

        TEXT = "text"
        PANDAS = "pandas"
        PSTATS = "pstats"

    def __init__(self, settings: Optional[ProfilerSettings] = None) -> None:
        """Initialize Profiler."""
        self.settings = settings if settings else ProfilerSettings()
        self._profiler: Any

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

    @abstractmethod
    def output(self, output_type: OutputType = OutputType.TEXT) -> Any:
        """Profiler.export.

        Exports profiler output in specified format.

        Args:
            output_type: Output type.

        Returns:
            Output in specified format.
        """

    @abstractmethod
    def print(self, verbose: bool = False) -> None:
        """Profiler.end.

        End profiling.

        Args:
            verbose: If True, prints more detailed info.

        Returns:
            Any
        """

    @abstractmethod
    def save(
        self, output_type: OutputType = OutputType.TEXT, filepath: str = "profkit.out"
    ) -> None:
        """Profiler.save.

        End profiling.

        Args:
            output_type: Output type.
            filepath: Path to file where output will be saved.

        Returns:
            Any
        """
