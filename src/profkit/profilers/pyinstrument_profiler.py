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

from typing import Any, Optional, Union

from loguru import logger
import pyinstrument

from profkit.profilers.profiler import Profiler


class PyInstrumentProfiler(Profiler):
    """PyInstrumentProfiler class.

    Args:
        arg: ...
    """

    def __init__(self, arg: Optional[Any] = None):
        """Initialize PyInstrumentProfiler."""
        super().__init__(arg)
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
