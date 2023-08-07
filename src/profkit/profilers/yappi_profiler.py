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
import os
from pathlib import Path
import pstats
import sys
from typing import Any, Optional, Union

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

    def output_to_text(self, verbose: bool = False, filepath: Optional[Union[str, Path]] = None) -> str:
        """YappiProfiler.output_to_text.

        Returns profiler output as text.

        Args:
            verbose: If True, outputs more detailed info.
            filepath: If specified, output is saved.

        Returns:
            Output as text.
        """
        string_stream = StringIO()
        self._profiler.get_func_stats().print_all(out=string_stream)
        if filepath:
            file_stream = open(filepath, "w")
            self._profiler.get_func_stats().print_all(out=file_stream)
        return string_stream.getvalue()

    def output_to_callgrind(self, filepath: Optional[Union[str, Path]] = None) -> Optional[list[str]]:
        """YappiProfiler.output_to_callgrind.

        Returns profiler output in callgrind format.

        Args:
            filepath: If specified, output is saved.

        Returns:
            Output in callgrind format.
        """
        output = self._to_callgrind()
        if filepath:
            with open(filepath, "w") as f:
                f.write("\n".join(output))
        return output

    def output_to_pstats(self, filepath: Optional[Union[str, Path]] = None) -> pstats.Stats:
        """YappiProfiler.output_to_pstats.

        Returns profiler output in pstats format.

        Args:
            filepath: If specified, output is saved.

        Returns:
            Output in pstats format.
        """
        stats = self._profiler.get_func_stats()
        if filepath:
            stats.save(path=filepath, type="pstat")
        return self._profiler.convert2pstats(stats)

    def print(self, verbose: bool = False) -> None:
        """YappiProfiler.print.

        Prints profiler output.

        Args:
            verbose: If True, outputs more detailed info.

        Returns:
            Any
        """
        self._profiler.get_func_stats().print_all()

    def _to_callgrind(self) -> list[str]:
        """Converts output to callgrind format"""
        stats = self._profiler.get_func_stats()
        # ================================================================================
        # Copy & paste from lines 928-966 in
        # https://github.com/sumerc/yappi/blob/1.4.0/yappi/yappi.py
        # ================================================================================
        # BEGIN PASTE
        # ================================================================================
        header = """version: 1\ncreator: %s\npid: %d\ncmd:  %s\npart: 1\n\nevents: Ticks""" % \
            ('yappi', os.getpid(), ' '.join(sys.argv))

        lines = [header]

        # add function definitions
        file_ids = ['']
        func_ids = ['']
        for func_stat in stats:
            file_ids += ['fl=(%d) %s' % (func_stat.index, func_stat.module)]
            func_ids += [
                'fn=(%d) %s %s:%s' % (
                    func_stat.index, func_stat.name, func_stat.module,
                    func_stat.lineno
                )
            ]

        lines += file_ids + func_ids

        # add stats for each function we have a record of
        for func_stat in stats:
            func_stats = [
                '',
                'fl=(%d)' % func_stat.index,
                'fn=(%d)' % func_stat.index
            ]
            func_stats += [
                '%s %s' % (func_stat.lineno, int(func_stat.tsub * 1e6))
            ]

            # children functions stats
            for child in func_stat.children:
                func_stats += [
                    'cfl=(%d)' % child.index,
                    'cfn=(%d)' % child.index,
                    'calls=%d 0' % child.ncall,
                    '0 %d' % int(child.ttot * 1e6)
                ]
            lines += func_stats
        # ================================================================================
        # END PASTE
        # ================================================================================
        return lines
