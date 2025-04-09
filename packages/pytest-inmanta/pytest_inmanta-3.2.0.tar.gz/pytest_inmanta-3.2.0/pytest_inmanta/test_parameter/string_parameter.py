"""
Copyright 2022 Inmanta

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

from pytest_inmanta.test_parameter.parameter import TestParameter


class StringTestParameter(TestParameter[str]):
    """
    A test parameter that should contain a string value.  The option will be
    store as a string, and resolved as is.

    .. code-block:: python

        inm_lsm_host = StringTestParameter(
            argument="--lsm-host",
            environment_variable="INMANTA_LSM_HOST",
            usage="Remote orchestrator to use for the remote_inmanta fixture",
            default="127.0.0.1",
            group=param_group,
        )

    """

    def validate(self, raw_value: object) -> str:
        return str(raw_value)
