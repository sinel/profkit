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

import cProfile
from contextlib import redirect_stdout
from io import StringIO
import pstats
from typing import Any, Optional

from profkit.profilers.profiler import Profiler
from profkit.settings import ProfilerSettings


class CProfileProfiler(Profiler):
    """CProfileProfiler class.

    Args:
        settings: Profiler settings.
    """

    def __init__(self, settings: Optional[ProfilerSettings] = None):
        """Initialize CProfileProfiler."""
        super().__init__(settings)
        self._profiler = cProfile.Profile()

    def begin(self) -> Any:
        """CProfileProfiler.begin.

        Begin profiling.

        Returns:
            Any
        """
        self._profiler.enable()

    def end(self) -> Any:
        """CProfileProfiler.end.

        End profiling.

        Returns:
            Any
        """
        self._profiler.disable()

    def output(
        self, output_type: Profiler.OutputType = Profiler.OutputType.TEXT
    ) -> Any:
        """CProfileProfiler.export.

        Exports profiler output in specified format.

        Args:
            output_type: Output type.

        Returns:
            Output in specified format.
        """
        pstats_obj = pstats.Stats(self._profiler)
        if output_type is Profiler.OutputType.PSTATS:
            return pstats_obj
        elif output_type is Profiler.OutputType.TEXT:
            print_output = StringIO()
            with redirect_stdout(print_output):
                pstats_obj.print_stats()
            return print_output
        else:
            raise ValueError(f"{Profiler.OutputType.PANDAS} is not yet supported.")

    def print(self, verbose: bool = False) -> None:
        """CProfileProfiler.end.

        End profiling.

        Args:
            verbose: If True, prints more detailed info.

        Returns:
            Any
        """
        pstats_obj = pstats.Stats(self._profiler)
        pstats_obj.print_stats()

    def save(
        self,
        output_type: Profiler.OutputType = Profiler.OutputType.TEXT,
        filepath: str = "profkit.out",
    ) -> None:
        """CProfileProfiler.save.

        End profiling.

        Args:
            output_type: Output type.
            filepath: Path to file where output will be saved.

        Returns:
            Any
        """
        pstats_obj = pstats.Stats(self._profiler)
        if output_type is Profiler.OutputType.PSTATS:
            pstats_obj.dump_stats(filepath)
        elif output_type is Profiler.OutputType.TEXT:
            with open(filepath, "w") as f:
                with redirect_stdout(f):
                    self.print()
        else:
            raise ValueError(f"{Profiler.OutputType.PANDAS} is not yet supported.")
