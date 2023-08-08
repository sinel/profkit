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
"""Unit test configuration."""
from __future__ import annotations

import logging
import random
import time
from typing import Callable, Generator, Optional

from loguru import logger
import pytest
from wonderwords import RandomWord


@pytest.fixture
def loguru_caplog(
    caplog: pytest.LogCaptureFixture,
) -> Generator[pytest.LogCaptureFixture, None, None]:
    """Fixture for capturing loguru logging output via ptest.

    Since pytest links to the standard library’s logging module,
    it is necessary to add a sink that propagates Loguru to the caplog handler.
    This is done by overriding the caplog fixture to capture its handler.
    See:
    https://loguru.readthedocs.io/en/stable/resources/migration.html#replacing-caplog-fixture-from-pytest-library

    Args:
        caplog: The pytest caplog fixture
        which captures logging output so that it can be tested against.
    """

    class PropagateHandler(logging.Handler):
        def emit(self, record: logging.LogRecord) -> None:
            logging.getLogger(record.name).handle(record)

    handler_id = logger.add(PropagateHandler(), format="{message}")
    yield caplog
    logger.remove(handler_id)


def random_function(name: Optional[str] = None) -> Callable:
    """Generates random test function."""
    choice = random.randint(0, 2)
    if choice == 0:
        return sleep_function(name)
    elif choice == 1:
        return loop_function(name)
    else:
        return generate_test_function("pass", name)


def sleep_function(name: Optional[str] = None) -> Callable:
    """Generates test function with sleep."""
    code = f"time.sleep({random.uniform(0.25, 1.0)})"
    return generate_test_function(code, name)


def loop_function(name: Optional[str] = None) -> Callable:
    """Generates test function with for loop."""
    code = f"for i in range({random.randint(1000000, 10000000)}): pass"
    return generate_test_function(code, name)


@pytest.fixture
def profiler_test_functions() -> list[Callable]:
    """Functions for testing profiler."""
    function_calls = []
    for i in range(random.randint(5, 10)):
        f = random_function(f"function{i}")
        for j in range(random.randint(1, 5)):
            f = generate_test_function(f"{f.__name__}()", f"function{i}_{j}")
        function_calls.append(f)
    return function_calls


def generate_test_function(code: str, name: Optional[str] = None) -> Callable:
    """Generates test function with specified name and code."""
    if name is None:
        name = f"{RandomWord().word(include_categories=['adjective'])}Function"
    code = f"""def {name}(*args, **kwargs):\n  {code}"""
    exec(code, globals(), locals())
    func: Callable = locals()[name]
    globals()[func.__name__] = func
    return func
