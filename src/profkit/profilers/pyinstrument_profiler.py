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

import pstats
from typing import Any, Optional

import pyinstrument
from pyinstrument.renderers import PstatsRenderer

from profkit.profilers.profiler import Profiler
from profkit.settings import ProfilerSettings


class PyInstrumentProfiler(Profiler):
    """PyInstrumentProfiler class.

    Args:
        settings: Profiler settings.
    """

    def __init__(self, settings: Optional[ProfilerSettings] = None):
        """Initialize PyInstrumentProfiler."""
        super().__init__(settings)
        self._profiler = pyinstrument.Profiler()

    def begin(self) -> Any:
        """PyInstrumentProfiler.begin.

        Begin profiling.

        Returns:
            Any
        """
        self._profiler.start()

    def end(self) -> Any:
        """PyInstrumentProfiler.end.

        End profiling.

        Returns:
            Any
        """
        self._profiler.stop()

    def output(
        self, output_type: Profiler.OutputType = Profiler.OutputType.TEXT
    ) -> Any:
        """PyInstrumentProfiler.export.

        Exports profiler output in specified format.

        Args:
            output_type: Output type.

        Returns:
            Output in specified format.
        """
        if output_type is Profiler.OutputType.PSTATS:
            return self._profiler.output(PstatsRenderer())
        elif output_type is Profiler.OutputType.TEXT:
            return self._profiler.output_text()
        else:
            raise ValueError(f"{Profiler.OutputType.PANDAS} is not yet supported.")

    def print(self, verbose: bool = False) -> None:
        """PyInstrumentProfiler.end.

        End profiling.

        Args:
            verbose: If True, prints more detailed info.

        Returns:
            Any
        """
        self._profiler.print()

    def save(
        self,
        output_type: Profiler.OutputType = Profiler.OutputType.TEXT,
        filepath: str = "profkit.out",
    ) -> None:
        """PyInstrumentProfiler.save.

        End profiling.

        Args:
            output_type: Output type.
            filepath: Path to file where output will be saved.

        Returns:
            Any
        """
        if output_type is Profiler.OutputType.PSTATS:
            output = self._profiler.output(PstatsRenderer())
            pstats_obj = pstats.Stats(output)
            pstats_obj.dump_stats(filepath)
        elif output_type is Profiler.OutputType.TEXT:
            with open(filepath, "w") as f:
                self._profiler.print(file=f)
        else:
            raise ValueError(f"{Profiler.OutputType.PANDAS} is not yet supported.")
