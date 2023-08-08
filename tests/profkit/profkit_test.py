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
"""Tests used for profkit."""
from __future__ import annotations

from loguru import logger
import pytest

from profkit.profilers.cprofile_profiler import CProfileProfiler
from profkit.profilers.profiler import Profiler
from profkit.profilers.pyinstrument_profiler import PyInstrumentProfiler
from profkit.profilers.yappi_profiler import YappiProfiler
from profkit.profkit import Profkit, about


def test_about(capsys: pytest.CaptureFixture) -> None:
    """Unit test for about."""
    about()
    captured = capsys.readouterr()
    all_outputs = captured.out.split("\n")
    python_version = all_outputs[-3]
    assert python_version == "Python Version:             3.11"


def test_init() -> None:
    """Unit test for Profkit.__init__."""
    profkit = Profkit()
    assert profkit.settings.default_profiler == "yappi"


def test_init_with_settings() -> None:
    """Unit test for Profkit.__init__."""
    profkit = Profkit({"default_profiler": "cprofile"})
    assert profkit.settings.default_profiler == "cprofile"


def test_add_profiler() -> None:
    """Unit test for Profkit.add_profiler."""
    profkit = Profkit()
    profiler = CProfileProfiler()
    profkit.add_profiler(profiler=profiler)
    assert list(profkit._profilers.values())[0] == profiler


def test_add_profiler_by_name() -> None:
    """Unit test for Profkit.add_profiler."""
    profkit = Profkit()
    profkit.add_profiler(name="test")
    assert isinstance(profkit._profilers["test"], YappiProfiler)


def test_get_profiler() -> None:
    """Unit test for Profkit.get_profiler."""
    profkit = Profkit()
    profkit.add_profiler(name="test")
    profiler = profkit.get_profiler("test")
    assert isinstance(profiler, YappiProfiler)


def test_has_profiler() -> None:
    """Unit test for Profkit.has_profiler."""
    profkit = Profkit()
    profkit.add_profiler(name="test")
    assert profkit.has_profiler("test")


def test_remove_profiler() -> None:
    """Unit test for Profkit.remove_profiler."""
    profkit = Profkit()
    profkit.add_profiler(name="test")
    assert profkit.has_profiler("test")
    profkit.remove_profiler(name="test")
    assert not profkit.has_profiler("test")


def test_create_cprofile_profiler() -> None:
    """Unit test for Profkit.create_profiler."""
    profkit = Profkit()
    profiler = profkit.create_profiler(Profkit.ProfilerLibrary.CPROFILE)
    assert isinstance(profiler, CProfileProfiler)


def test_create_pyinstrument_profiler() -> None:
    """Unit test for Profkit.create_profiler."""
    profkit = Profkit()
    profiler = profkit.create_profiler(Profkit.ProfilerLibrary.PYINSTRUMENT)
    assert isinstance(profiler, PyInstrumentProfiler)


def test_create_yappi_profiler() -> None:
    """Unit test for Profkit.create_profiler."""
    profkit = Profkit()
    profiler = profkit.create_profiler(Profkit.ProfilerLibrary.YAPPI)
    assert isinstance(profiler, YappiProfiler)


def test_profile() -> None:
    """Unit test for Profkit.profile decorator."""
    profkit = Profkit()

    @profkit.profile()
    def dummy_function() -> None:
        pass

    dummy_function()
    assert isinstance(profkit._profilers["dummy_function"], Profiler)


def test_profile_with_callback(capsys: pytest.CaptureFixture) -> None:
    """Unit test for Profkit.profile decorator with callback."""
    profkit = Profkit()

    def print_profiler_type(profiler: Profiler) -> None:
        print(f"PROFILER NAME = {profiler.__class__.__name__}")

    @profkit.profile(callback=print_profiler_type)
    def dummy_function() -> None:
        pass

    dummy_function()
    assert isinstance(profkit._profilers["dummy_function"], Profiler)
    captured = capsys.readouterr()
    assert captured.out.rstrip() == "PROFILER NAME = YappiProfiler"
