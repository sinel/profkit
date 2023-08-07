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

from pathlib import Path
import pstats
from typing import Any, Optional, Union
import warnings

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

    def output_to_text(self, verbose: bool = False, filepath: Optional[Union[str, Path]] = None) -> str:
        """PyInstrumentProfiler.output_to_text.

        Returns profiler output as text.

        Args:
            verbose: If True, outputs more detailed info.
            filepath: If specified, output is saved.

        Returns:
            Output as text.
        """
        if filepath:
            with open(filepath, "w") as f:
                self._profiler.print(file=f)
        return self._profiler.output_text()

    def output_to_callgrind(self, filepath: Optional[Union[str, Path]] = None) -> Optional[list[str]]:
        """CProfileProfiler.output_to_callgrind.

        Returns profiler output in callgrind format.

        Args:
            filepath: If specified, output is saved.

        Returns:
            Output in callgrind format.
        """
        warnings.warn("Output to callgrind format is not supported for CProfile profiler.")
        return None

    def output_to_pstats(self, filepath: Optional[Union[str, Path]] = None) -> pstats.Stats:
        """PyInstrumentProfiler.output_to_pstats.

        Returns profiler output in pstats format.

        Args:
            filepath: If specified, output is saved.

        Returns:
            Output in pstats format.
        """
        output = self._profiler.output(PstatsRenderer())
        pstats_obj = pstats.Stats(output)
        if filepath:
            pstats_obj.dump_stats(filepath)
        return pstats_obj

    def print(self, verbose: bool = False) -> None:
        """PyInstrumentProfiler.print.

        Prints profiler output.

        Args:
            verbose: If True, outputs more detailed info.

        Returns:
            Any
        """
        self._profiler.print()
