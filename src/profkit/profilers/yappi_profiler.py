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

from contextlib import redirect_stdout
from io import StringIO
from typing import Any, Optional

import yappi

from profkit.profilers.profiler import Profiler
from profkit.settings import ProfilerSettings


class YappiProfiler(Profiler):
    """YappiProfiler class.

    Args:
        settings: Profiler settings.
    """

    def __init__(self, settings: Optional[ProfilerSettings] = None):
        """Initialize Profiler."""
        super().__init__(settings)
        self._profiler = yappi

    def begin(self) -> Any:
        """YappiProfiler.begin.

        Begin profiling.

        Returns:
            Any
        """
        self._profiler.start()

    def end(self) -> Any:
        """YappiProfiler.end.

        End profiling.

        Returns:
            Any
        """
        self._profiler.stop()

    def output(
        self, output_type: Profiler.OutputType = Profiler.OutputType.TEXT
    ) -> Any:
        """YappiProfiler.export.

        Exports profiler output in specified format.

        Args:
            output_type: Output type.

        Returns:
            Output in specified format.
        """
        if output_type is Profiler.OutputType.PSTATS:
            return self._profiler.convert2pstats(self._profiler.get_func_stats())
        elif output_type is Profiler.OutputType.TEXT:
            print_output = StringIO()
            with redirect_stdout(print_output):
                self._profiler.get_func_stats().print_all()
            return print_output
        else:
            raise ValueError(f"{Profiler.OutputType.PANDAS} is not yet supported.")

    def print(self, verbose: bool = False) -> None:
        """YappiProfiler.end.

        End profiling.

        Args:
            verbose: If True, prints more detailed info.

        Returns:
            Any
        """
        self._profiler.get_func_stats().print_all()

    def save(
        self,
        output_type: Profiler.OutputType = Profiler.OutputType.TEXT,
        filepath: str = "profkit.out",
    ) -> None:
        """YappiProfiler.save.

        End profiling.

        Args:
            output_type: Output type.
            filepath: Path to file where output will be saved.

        Returns:
            Any
        """
        if output_type is Profiler.OutputType.PSTATS:
            self._profiler.get_func_stats().save(path=filepath, type="pstat")
        elif output_type is Profiler.OutputType.TEXT:
            with open(filepath, "w") as f:
                with redirect_stdout(f):
                    self._profiler.get_func_stats().print_all()
        else:
            raise ValueError(f"{Profiler.OutputType.PANDAS} is not yet supported.")
