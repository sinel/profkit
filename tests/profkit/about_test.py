#  ********************************************************************************
#
#    _________ __________ _
#   / ___/ __ `/ ___/ __ `/    Python toolkit
#  / /__/ /_/ (__  ) /_/ /     for control and analysis
#  \___/\__,_/____/\__, /      of superconducting qubits
#                    /_/
#
#  Copyright (c) 2023 Sinan Inel <sinan.inel@aalto.fi>
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
"""Tests used for debugging."""
from __future__ import annotations

from loguru import logger
from pytest import CaptureFixture

from profkit.about import about


def test_about(capsys: CaptureFixture) -> None:
    """Unit test for about."""
    about()
    captured = capsys.readouterr()
    all_outputs = captured.out.split("\n")
    logger.debug(all_outputs)
    python_version = all_outputs[-3]
    logger.debug(python_version)
    assert python_version == "Python Version:             3.11"
