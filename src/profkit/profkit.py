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
"""Profkit."""
from __future__ import annotations

from enum import StrEnum
import functools
from pathlib import Path
from typing import Any, Callable, Optional, Union

from pydantic_yaml import parse_yaml_file_as
from wonderwords import RandomWord

from profkit.profilers.cprofile_profiler import CProfileProfiler
from profkit.profilers.profiler import Profiler
from profkit.profilers.pyinstrument_profiler import PyInstrumentProfiler
from profkit.profilers.yappi_profiler import YappiProfiler
from profkit.settings import Settings


class Profkit:
    """Profkit class.

    Args:
        settings: Profkit settings.
        filepath: Relative filepath to yaml settings file.
    """

    class ProfilerLibrary(StrEnum):
        """Profiler library enumeration."""

        CPROFILE = "cprofile"
        PYINSTRUMENT = "pyinstrument"
        YAPPI = "yappi"

    def __init__(
        self,
        settings: Optional[dict[str, Any]] = None,
        filepath: str = "profkit.yaml",
    ):
        """Initialize Profiler."""
        settings_file = Path(__file__).parent / filepath
        if not settings_file.is_file():
            self.settings = parse_yaml_file_as(Settings, settings_file)
        else:
            self.settings = Settings()
        self.settings = self.settings.model_copy(update=settings, deep=True)
        self._profilers: dict[str, Profiler] = {}

    def has_profiler(self, name: str) -> bool:
        """Checks if profkit instance has profiler.

        Args:
            name: Profiler name. Must be unique within scope of Profkit instance.
        """
        return name in self._profilers

    def get_profiler(self, name: str) -> Optional[Profiler]:
        """Gets profiler.

        Args:
            name: Profiler name. Must be unique within scope of Profkit instance.
        """
        return self._profilers.get(name, None)

    def add_profiler(
        self,
        name: Optional[str] = None,
        profiler: Optional[Union[Profiler, ProfilerLibrary]] = None,
    ) -> tuple[str, Profiler]:
        """Adds profiler.

        Args:
            name: Profiler name. Must be unique within scope of Profkit instance.
            profiler: Profiler instance
                or profiler library to use for creating new profiler instance.
        """
        if name is None:
            name = f"{RandomWord().word(include_categories=['adjective'])}Profiler"
        if isinstance(profiler, Profiler):
            self._profilers[name] = profiler
        else:
            profiler = self.create_profiler(profiler)
            self._profilers[name] = profiler
        return name, profiler

    def remove_profiler(self, name: str) -> None:
        """Removes profiler.

        Args:
            name: Profiler name. Must be unique within scope of Profkit instance.
        """
        del self._profilers[name]

    def create_profiler(
        self, profiler_library: Optional[ProfilerLibrary] = None
    ) -> Profiler:
        """Creates profiler.

        Args:
            profiler_library: Profiler library.

        Returns:
            :py:class:`profkit.profiler.Profiler`
        """
        if profiler_library is None:
            profiler_library = Profkit.ProfilerLibrary(self.settings.profiler.default)
        if profiler_library is Profkit.ProfilerLibrary.CPROFILE:
            return CProfileProfiler(self.settings.profiler)
        elif profiler_library is Profkit.ProfilerLibrary.PYINSTRUMENT:
            return PyInstrumentProfiler(self.settings.profiler)
        elif profiler_library is Profkit.ProfilerLibrary.YAPPI:
            return YappiProfiler(self.settings.profiler)
        else:
            raise ValueError(f"Unsupported profiler library: {profiler_library.name}.")

    def profile(
        self,
        library: Optional[ProfilerLibrary] = None,
        callback: Optional[Callable[[Profiler], None]] = None,
    ) -> Any:
        """Decorator for profiling the execution of a function.

        Args:
            library: Profiler library.
            callback: Callback function to process profiler results.

        Returns:
            Wrapper function for decorator.
        """

        def wrapper(func: Callable) -> Any:
            @functools.wraps(func)
            def wrapped(*args: Any, **kwargs: Any) -> Any:
                _, profiler = self.add_profiler(func.__name__, library)
                profiler.begin()
                result = func(*args, **kwargs)
                profiler.end()
                if callback:
                    callback(profiler)
                return result

            return wrapped

        return wrapper


def about() -> None:
    """Provides information about profkit."""
    print(
        "================================================================================"
    )
    print(
        "Profkit: Python toolkit for using profilers "
        "with support for filtering, analysis and visualization"
    )
    print(
        "================================================================================"
    )
    print("Copyright (c) 2023 Sinan Inel <sinan.inel@farsimple.com>.")
    print("")
    print(f"Source:                    https://github.com/sinel/profkit")
    print("Version:                    0.1.0")
    print("Python Version:             3.11")
    print(
        "================================================================================"
    )


if __name__ == "__main__":
    about()
