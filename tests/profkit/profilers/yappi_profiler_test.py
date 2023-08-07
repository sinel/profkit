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

import os
from pathlib import Path
import pstats

from loguru import logger
import pytest
from typing import Callable

from profkit.profilers.yappi_profiler import YappiProfiler

HEADERS = "name                                  ncall  tsub      ttot      tavg"


def test_profiler(
    profiler_test_functions: list[Callable], capsys: pytest.CaptureFixture
) -> None:
    """Unit test for YappiProfiler."""
    profiler = YappiProfiler()
    profiler.begin()
    for f in profiler_test_functions:
        f()
    profiler.end()


def test_output_to_text(
    profiler_test_functions: list[Callable], capsys: pytest.CaptureFixture
) -> None:
    """Unit test for YappiProfiler.output_to_text."""
    profiler = YappiProfiler()
    profiler.begin()
    for f in profiler_test_functions:
        f()
    profiler.end()
    output = profiler.output_to_text()
    assert HEADERS in output


def test_output_to_text_file(
    profiler_test_functions: list[Callable], capsys: pytest.CaptureFixture, tmp_path: Path
) -> None:
    """Unit test for YappiProfiler.output_to_text with file."""
    profiler = YappiProfiler()
    profiler.begin()
    for f in profiler_test_functions:
        f()
    profiler.end()
    filepath = tmp_path / "test.out"
    profiler.output_to_text(filepath=filepath)
    output = filepath.read_text()
    assert HEADERS in output


def test_output_to_callgrind(
    profiler_test_functions: list[Callable], capsys: pytest.CaptureFixture
) -> None:
    """Unit test for YappiProfiler.output_to_callgrind."""
    profiler = YappiProfiler()
    profiler.begin()
    for f in profiler_test_functions:
        f()
    profiler.end()
    output = profiler.output_to_callgrind()
    logger.debug(output)


def test_output_to_pstats(
    profiler_test_functions: list[Callable], capsys: pytest.CaptureFixture
) -> None:
    """Unit test for YappiProfiler.output_to_pstats."""
    profiler = YappiProfiler()
    profiler.begin()
    for f in profiler_test_functions:
        f()
    profiler.end()
    output = profiler.output_to_pstats()
    assert isinstance(output, pstats.Stats)


def test_output_to_pstats_file(
    profiler_test_functions: list[Callable], capsys: pytest.CaptureFixture, tmp_path: Path
) -> None:
    """Unit test for YappiProfiler.output_to_pstats with file."""
    profiler = YappiProfiler()
    profiler.begin()
    for f in profiler_test_functions:
        f()
    profiler.end()
    filepath = tmp_path / "test.out"
    profiler.output_to_pstats(filepath=filepath)
    stats = pstats.Stats(str(filepath.absolute()))
    stats.print_stats()


def test_print(
    profiler_test_functions: list[Callable], capsys: pytest.CaptureFixture
) -> None:
    """Unit test for YappiProfiler.print."""
    profiler = YappiProfiler()
    profiler.begin()
    for f in profiler_test_functions:
        f()
    profiler.end()
    profiler.print()
    captured = capsys.readouterr()
    logger.debug(f"CAPTURED = {captured}")
    all_outputs = captured.out.split(os.linesep)
    logger.debug(f"SIZE = {len(all_outputs)}")
    headers = all_outputs[4]
    assert headers == HEADERS
