"""
Copyright 2019 Inmanta

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Contact: code@inmanta.com
"""

# Note: These tests only function when the pytest output is not modified by plugins such as pytest-sugar!


def test_basic_example(testdir):
    """Make sure that our plugin works."""

    testdir.copy_example("testmodule")

    result = testdir.runpytest("tests/test_resource_run_v2.py")

    result.assert_outcomes(passed=2)
