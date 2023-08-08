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
from pathlib import Path
import pstats
import sys
from typing import Any, Optional, Union
import warnings

from loguru import logger

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
        self._profiler.create_stats()

    def output_to_text(
        self, verbose: bool = False, filepath: Optional[Union[str, Path]] = None
    ) -> str:
        """CProfileProfiler.output_to_text.

        Returns profiler output as text.

        Args:
            verbose: If True, outputs more detailed info.
            filepath: If specified, output is saved.

        Returns:
            Output as text.
        """
        string_stream = StringIO()
        pstats_string = pstats.Stats(self._profiler, stream=string_stream)
        pstats_string.print_stats()
        if filepath:
            file_stream = open(filepath, "w")
            pstats_file = pstats.Stats(self._profiler, stream=file_stream)
            pstats_file.print_stats()
        return string_stream.getvalue()

    def output_to_callgrind(
        self, filepath: Optional[Union[str, Path]] = None
    ) -> Optional[list[str]]:
        """CProfileProfiler.output_to_callgrind.

        Returns profiler output in callgrind format.

        Args:
            filepath: If specified, output is saved.

        Returns:
            Output in callgrind format.
        """
        warnings.warn(
            "Output to callgrind format is not supported for CProfile profiler."
        )
        return None

    def output_to_pstats(
        self, filepath: Optional[Union[str, Path]] = None
    ) -> pstats.Stats:
        """CProfileProfiler.output_to_pstats.

        Returns profiler output in pstats format.

        Args:
            filepath: If specified, output is saved.

        Returns:
            Output in pstats format.
        """
        pstats_obj = pstats.Stats(self._profiler)
        if filepath:
            pstats_obj.dump_stats(filepath)
        return pstats_obj

    def print(self, verbose: bool = False) -> None:
        """CProfileProfiler.print.

        Prints profiler output.

        Args:
            verbose: If True, outputs more detailed info.

        Returns:
            Any
        """
        pstats_obj = pstats.Stats(self._profiler)
        pstats_obj.print_stats()
