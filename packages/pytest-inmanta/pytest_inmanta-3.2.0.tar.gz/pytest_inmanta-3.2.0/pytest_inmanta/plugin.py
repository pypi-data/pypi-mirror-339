"""
Copyright 2021 Inmanta

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

import collections
import importlib
import inspect
import itertools
import json
import logging
import math
import os
import re
import shutil
import sys
import tempfile
import typing
import warnings
from collections import defaultdict
from dataclasses import dataclass
from itertools import chain
from pathlib import Path
from textwrap import dedent
from types import FunctionType, ModuleType
from typing import Dict, Iterator, List, Optional, Sequence, Set, Tuple

import pydantic
import pytest
import yaml
from tornado import ioloop

import inmanta.ast
from inmanta import compiler, config, const, module, plugins, protocol
from inmanta.agent import cache
from inmanta.agent import config as inmanta_config
from inmanta.agent import handler
from inmanta.agent.cache import AgentCache
from inmanta.agent.handler import (
    HandlerAPI,
    HandlerContext,
    LoggerABC,
    PythonLogger,
    ResourceHandler,
)
from inmanta.const import ResourceState
from inmanta.data import LogLine
from inmanta.data.model import AttributeStateChange, ResourceIdStr
from inmanta.env import PackageNotFound
from inmanta.execute.proxy import DynamicProxy
from inmanta.export import Exporter, ResourceDict, cfg_env
from inmanta.resources import Resource
from pytest_inmanta.core import (
    SUPPORTS_LEGACY_PROJECT_PIP_INDEX,
    SUPPORTS_PROJECT_PIP_INDEX,
)
from pytest_inmanta.test_parameter.parameter import ValueSetBy

PIP_NO_SOURCE_WARNING = (
    "No pip config source is configured, any attempt to perform a pip install will fail. "
    "Please set either one of the options --pip-index-url, --pip-use-system-config or "
    "one of the environment variables PIP_INDEX_URL or INMANTA_PIP_USE_SYSTEM_CONFIG"
)

if typing.TYPE_CHECKING:
    # Local type stub for mypy that works with both pytest < 7 and pytest >=7
    # https://docs.pytest.org/en/7.1.x/_modules/_pytest/legacypath.html#TempdirFactory
    import py

    class TempdirFactory:
        def mktemp(self, path: str) -> py.path.local:
            pass


if SUPPORTS_LEGACY_PROJECT_PIP_INDEX:
    from inmanta.module import ProjectPipConfig

import pytest_inmanta.parameters as parameters
from pytest_inmanta.handler import DATA
from pytest_inmanta.parameters import (
    inm_mod_in_place,
    inm_mod_repo,
    inm_no_load_plugins,
    inm_no_strict_deps_check,
    inm_venv,
)
from pytest_inmanta.test_parameter import (
    ParameterNotSetException,
    TestParameterRegistry,
)

try:
    """
    Those classes are only used in type annotation, but the import doesn't work
    in python 3.6.  So we simply catch the error and ignore it.
    """
    from pytest import CaptureFixture, Parser
except ImportError:
    pass

CURDIR = os.getcwd()
LOGGER = logging.getLogger()
SYS_EXECUTABLE = sys.executable

DEFAULT = object()


def pytest_addoption(parser: "Parser") -> None:
    TestParameterRegistry.pytest_addoption(parser)


def get_module() -> typing.Tuple[module.Module, str]:
    """
    Returns the module instance for the module being tested, as well as the path to its root.
    For v2 modules, the returned path is the same as the module's path attribute.
    """

    def find_module(path: str) -> typing.Optional[typing.Tuple[module.Module, str]]:
        mod: typing.Optional[module.Module]
        if hasattr(module.Module, "from_path"):
            mod = module.Module.from_path(path)
        else:
            # older versions of inmanta-core
            try:
                mod = module.Module(project=None, path=path)
            except module.InvalidModuleException:
                mod = None
        if mod is not None:
            return mod, path
        parent: str = os.path.dirname(path)
        return find_module(parent) if parent != path else None

    mod_info: typing.Optional[typing.Tuple[module.Module, str]] = find_module(CURDIR)
    if mod_info is None:
        raise Exception(
            "Module test case have to be saved in the module they are intended for. "
            "%s not part of module path" % CURDIR
        )
    return mod_info


@pytest.fixture()
def inmanta_plugins(
    project: "Project",
) -> typing.Iterator["InmantaPluginsImportLoader"]:
    importer: InmantaPluginsImporter = InmantaPluginsImporter(project)
    yield importer.loader


@pytest.fixture()
def project(
    project_shared: "Project", capsys: "CaptureFixture", inmanta_state_dir: str
) -> typing.Iterator["Project"]:
    DATA.clear()
    project_shared.clean()
    project_shared.init(capsys)

    # Set the state dir after initializing the project, as it reloads the
    # config which would overwrite our setting
    config.state_dir.set(inmanta_state_dir)

    yield project_shared
    project_shared.clean()


@pytest.fixture()
def project_no_plugins(
    project_shared_no_plugins: "Project",
    capsys: "CaptureFixture",
    inmanta_state_dir: str,
) -> typing.Iterator["Project"]:
    warnings.warn(
        DeprecationWarning(
            "The project_no_plugins fixture is deprecated in favor of the %s environment variable."
            % inm_no_load_plugins.environment_variable
        )
    )
    DATA.clear()
    project_shared_no_plugins.clean()
    project_shared_no_plugins.init(capsys)

    # Set the state dir after initializing the project, as it reloads the
    # config which would overwrite our setting
    config.state_dir.set(inmanta_state_dir)

    yield project_shared_no_plugins
    project_shared_no_plugins.clean()


def get_module_data(filename: str) -> str:
    """
    Get the given filename from the module directory in the source tree
    """
    current_path = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(current_path, "module", filename), "r") as fd:
        return fd.read()


@pytest.fixture(scope="session")
def project_shared(
    project_factory: typing.Callable[[typing.Dict[str, typing.Any]], "Project"],
) -> Iterator["Project"]:
    """
    A test fixture that creates a new inmanta project with the current module in. The returned object can be used
    to add files to the unittest module, compile a model and access the results, stdout and stderr.
    """
    yield project_factory()


# Temporary workaround for plugins loading multiple times (inmanta/pytest-inmanta#49)
@pytest.fixture(scope="session")
def project_shared_no_plugins(
    project_factory: typing.Callable[[typing.Dict[str, typing.Any]], "Project"],
) -> Iterator["Project"]:
    """
    A test fixture that creates a new inmanta project with the current module in. The returned object can be used
    to add files to the unittest module, compile a model and access the results, stdout and stderr.
    This project is initialized with load_plugins == False.
    """
    yield project_factory(load_plugins=False)


def get_project_repos(repo_options: typing.Sequence[str]) -> typing.Sequence[object]:
    """
    Returns the list of repos for the project as a serializable object. For recent versions of core, includes repo types.

    :param repo_options: The desired repos as plain strings in the form "[<type>:]<url>". If type is omitted, defaults to git
        for backwards compatibility. Explicitly passing type is only supported for inmanta versions that accept type in the
        project metadata.
    """

    def parse_repo(repo_str: str) -> object:
        parts: typing.Sequence[str] = repo_str.split(":", maxsplit=1)
        if not hasattr(module, "ModuleRepoType"):
            # compatibility mode
            return repo_str
        else:
            repo_info: module.ModuleRepoInfo
            try:
                repo_info = module.ModuleRepoInfo(url=parts[1], type=parts[0])
            # there might be only one part or part might be just "https"
            except (IndexError, pydantic.ValidationError):
                repo_info = module.ModuleRepoInfo(url=repo_str)
            if SUPPORTS_LEGACY_PROJECT_PIP_INDEX:
                if repo_info.type == module.ModuleRepoType.package:
                    alternative_text: str = (
                        "is now deprecated and will raise a warning during compilation."
                        " Use the --pip-index-url <index_url> pytest option instead or set"
                        " the %s environment variable to address these warnings. "
                    )
                    if inm_mod_repo._value_set_using == ValueSetBy.ENV_VARIABLE:
                        LOGGER.warning(
                            "Setting a package source through the %s environment variable "
                            + alternative_text,
                            inm_mod_repo.environment_variable,
                            parameters.pip_index_url.environment_variable,
                        )
                    elif inm_mod_repo._value_set_using == ValueSetBy.CLI:
                        LOGGER.warning(
                            "Setting a package source through the --module-repo <index_url> cli option with type `package` "
                            + alternative_text,
                            parameters.pip_index_url.environment_variable,
                        )

            return repo_info.model_dump(mode="json")

    return [parse_repo(repo) for repo in repo_options]


@pytest.fixture(scope="session")
def project_dir() -> str:
    """
    Returns the directory that will be used by the project_factory fixture to store the Inmanta project.
    """
    project_dir_path = tempfile.mkdtemp()

    yield project_dir_path

    try:
        shutil.rmtree(project_dir_path)
    except PermissionError:
        LOGGER.warning(
            "Cannot cleanup test project %s. This can be caused because we try to remove a virtual environment, "
            "loaded by this python process. Try to use a shared environment with --venv",
            project_dir_path,
        )


@pytest.fixture(scope="session")
def project_metadata(request: pytest.FixtureRequest) -> module.ProjectMetadata:
    """
    This fixture returns the metadata object that will be used to create the project used in
    all test cases using the project fixture.

    This fixture can be overwritten in specific modules to modify the project.yml file
    that should be used there (i.e. set the agent_install_dependency_modules option)
    """
    repo_options = inm_mod_repo.resolve(request.config)
    repos: typing.Sequence[object] = get_project_repos(
        chain.from_iterable(
            repo.split(" ")
            for repo in (
                repo_options if isinstance(repo_options, list) else [repo_options]
            )
        )
    )

    index_urls: Sequence[str] = parameters.pip_index_url.resolve(request.config)
    repos_urls: List[str] = [
        repo["url"]
        for repo in repos
        if repo["type"] == module.ModuleRepoType.package.value
    ]

    pip_use_system_config = parameters.pip_use_system_config.resolve(request.config)
    pip_pre = parameters.pip_pre.resolve(request.config)

    modulepath = ["libs"]
    in_place = inm_mod_in_place.resolve(request.config)
    if in_place:
        modulepath.append(str(Path(CURDIR).parent))

    if SUPPORTS_PROJECT_PIP_INDEX:
        # Backward compat: translate repo url to index url
        index_urls = list(index_urls) + repos_urls
        if index_urls:
            index_url = index_urls[0]
            extra_index_url = index_urls[1:]
        else:
            index_url = None
            extra_index_url = []

        pip_config: ProjectPipConfig = ProjectPipConfig(
            index_url=index_url,
            extra_index_url=extra_index_url,
            use_system_config=pip_use_system_config,
            pre=pip_pre,
        )

        if not pip_config.has_source():
            LOGGER.warning(PIP_NO_SOURCE_WARNING)

        return module.ProjectMetadata(
            name="testcase",
            description="Project for testcase",
            repo=repos,
            modulepath=modulepath,
            downloadpath="libs",
            install_mode=parameters.inm_install_mode.resolve(request.config).value,
            pip=pip_config,
        )
    elif SUPPORTS_LEGACY_PROJECT_PIP_INDEX:
        # On newer versions of core we set the pip.index_url of the project.yml file
        pip_config: ProjectPipConfig = ProjectPipConfig(
            # This ensures no duplicates are returned and insertion order is preserved.
            # i.e. the left-most index will be passed to pip as --index-url and the others as --extra-index-url
            index_urls=list(
                {value: None for value in itertools.chain(index_urls, repos_urls)}
            )
        )
        return module.ProjectMetadata(
            name="testcase",
            description="Project for testcase",
            repo=repos,
            modulepath=modulepath,
            downloadpath="libs",
            install_mode=parameters.inm_install_mode.resolve(request.config).value,
            pip=pip_config,
        )
    else:
        if index_urls:
            LOGGER.warning(
                "Setting a project-wide pip index is not supported on this version of inmanta-core. "
                "The provided index will be used as a v2 package source"
            )
        v2_source_repos = [
            {"url": index_url, "type": "package"} for index_url in index_urls
        ]
        return module.ProjectMetadata(
            name="testcase",
            description="Project for testcase",
            repo=list(repos) + v2_source_repos,
            modulepath=modulepath,
            downloadpath="libs",
            install_mode=parameters.inm_install_mode.resolve(request.config).value,
        )


@pytest.fixture(scope="session")
def project_factory(
    request: pytest.FixtureRequest,
    project_dir: str,
    project_metadata: module.ProjectMetadata,
) -> typing.Callable[[], "Project"]:
    """
    A factory that constructs a single Project.
    """
    _sys_path = sys.path
    os.mkdir(os.path.join(project_dir, "libs"))

    try:
        env_override: Optional[str] = str(inm_venv.resolve(request.config))
    except ParameterNotSetException:
        env_override = None
    env_dir = os.path.join(project_dir, ".env")
    if env_override and not os.path.isdir(env_override):
        raise Exception(f"Specified venv {env_override} does not exist")
    if env_override is not None:
        try:
            os.symlink(os.path.abspath(env_override), env_dir)
        except OSError:
            LOGGER.exception(
                "Unable to use shared env (symlink creation from %s to %s failed).",
                env_override,
                os.path.join(project_dir, ".env"),
            )
            raise

    with open(os.path.join(project_dir, "project.yml"), "w+") as fd:
        yaml.safe_dump(project_metadata.model_dump(mode="json"), fd)

    ensure_current_module_install(
        os.path.join(project_dir, "libs"),
        in_place=inm_mod_in_place.resolve(request.config),
    )

    def create_project(**kwargs: object):
        load_plugins = not inm_no_load_plugins.resolve(request.config)
        no_strict_deps_check = inm_no_strict_deps_check.resolve(request.config)
        extended_kwargs: typing.Dict[str, object] = {
            "no_strict_deps_check": no_strict_deps_check,
            "load_plugins": load_plugins,
            "env_path": env_dir,
            **kwargs,
        }
        try:
            test_project = Project(project_dir, **extended_kwargs)
        except PackageNotFound as e:
            if "pip is not configured" in str(e):
                raise PackageNotFound(PIP_NO_SOURCE_WARNING) from e
            raise

        # create the unittest module
        test_project.create_module(
            "unittest",
            initcf=get_module_data("init.cf"),
            initpy=get_module_data("init.py"),
        )

        return test_project

    yield create_project

    sys.path = _sys_path


def ensure_current_module_install(v1_modules_dir: str, in_place: bool = False) -> None:
    """
    Ensures that the current module is installed: if it is a v1 module, adds it to the modules path, otherwise verifies that it
    has been installed.
    """
    # copy the current module in
    mod: module.Module
    path: str
    mod, path = get_module()
    if not hasattr(module, "ModuleV2") or isinstance(mod, module.ModuleV1):
        if not in_place:
            shutil.copytree(
                path,
                os.path.join(v1_modules_dir, mod.name),
                ignore=shutil.ignore_patterns("__pycache__"),
            )
    else:
        installed: typing.Optional[module.ModuleV2] = module.ModuleV2Source(
            urls=[]
        ).get_installed_module(None, mod.name)
        if installed is None:
            raise Exception(
                "The module being tested is not installed in the current Python environment. Please install it with"
                " `pip install -e .` before running the tests."
            )
        if not installed.is_editable():
            LOGGER.warning(
                "The module being tested is not installed in editable mode. As a result the tests will not pick up any changes"
                " to the local source files. To install it in editable mode, run `pip install -e .`."
            )


class MockProcess(object):
    """
    A mock agentprocess
    """

    def __init__(self):
        self._io_loop = ioloop.IOLoop.current()


class MockAgent(object):
    """
    A mock agent for unit testing
    """

    def __init__(self, uri):
        self.uri = uri
        self._env_id = cfg_env.get()
        self.sessionid = "mockid"
        self.environment = self._env_id
        # This is for the new old api in inmanta.agent.agent.AgentInstance
        self.process = MockProcess()
        # This is for the new agent api in inmanta.agent.executor.AgentInstance
        self.eventloop = self.process._io_loop


class MockClient(object):
    """
    A mock object for Handler._client

    It should be of type inmanta.protocol.endpoints.SessionClient
    However, we chose to only mock those functions we expect to see used.

    Any unexpected use of the client will cause an attribute error.
    This will prevent any unexpected/unsafe attempts to reach an orchestrator
    """

    def __init__(self):
        self.discovered_resources: list[object] = []

    async def discovered_resource_create_batch(
        self, tid, discovered_resources: collections.abc.Sequence[object]
    ) -> protocol.Result:
        """
        Mock function for inmanta.protocol.methodsv2.discovered_resource_create_batch

        Collects all discovered resources
        """
        self.discovered_resources.extend(discovered_resources)
        return inmanta.protocol.common.Result(200)


class InmantaPluginsImportLoader:
    """
    Makes inmanta_plugins packages (Python source for inmanta modules) available dynamically so that tests can use them
    safely without having to refresh imports when the compiler is reset.
    """

    def __init__(self, importer: "InmantaPluginsImporter") -> None:
        self._importer: InmantaPluginsImporter = importer

    def __getattr__(self, name: str):
        submodules: typing.Optional[typing.Dict[str, ModuleType]] = (
            self._importer.get_submodules(name)
        )
        fq_mod_name: str = f"inmanta_plugins.{name}"
        if submodules is None or fq_mod_name not in submodules:
            raise AttributeError("No inmanta module named %s" % name)
        return submodules[fq_mod_name]


class InmantaPluginsImporter:
    def __init__(self, project: "Project") -> None:
        self.project: Project = project
        self.loader: InmantaPluginsImportLoader = InmantaPluginsImportLoader(self)

    def get_submodules(
        self, module_name: str
    ) -> typing.Optional[typing.Dict[str, ModuleType]]:
        inmanta_project: module.Project = module.Project.get()
        if not inmanta_project.loaded:
            raise Exception(
                "Dynamically importing from inmanta_plugins requires a loaded inmanta.module.Project. Make sure to use the"
                " project fixture."
            )
        modules: typing.Dict[str, module.Module] = inmanta_project.get_modules()
        if module_name not in modules:
            return None
        result = {}
        importlib.invalidate_caches()
        for _, fq_submod_name in modules[module_name].get_plugin_files():
            result[str(fq_submod_name)] = importlib.import_module(str(fq_submod_name))
        return result


class ProjectLoader:
    """
    Singleton providing methods for managing project loading and associated side effects. Since these operations have global
    side effects, managing them calls for a centralized manager rather than managing them on the Project instance level.

    This class manages the setting and loading of a project, as well as the following side effects:
        - Python modules: under normal operation, an inmanta module's Python modules are loaded when the project is loaded.
            However, to support top-level Python imports in test cases, pytest-inmanta instructs the project to not clean
            up loaded Python modules when setting a new project as this would force a reload, changing object identities.
            One exception is when working with dynamic modules whose content might change between project loads (for example
            the unittest module and any module created with Project.create_module). Therefore any dynamic modules are always
            forcefully cleaned up, forcing a reload when next imported.
        - Python module state: since Python module objects are kept alive (see above), any state kept on those objects is
            carried over accross compiles. To start each compile from a fresh state, any stateful modules must define one or
            more cleanup functions. This class is responsible for calling these functions when appropriate.
        - plugins: under normal operation, loading a project registers all modules' plugins as a side effect of loading each
            module's Python modules. However, pytest-inmanta does not reload said Python modules (see above). To make sure only
            loaded modules' plugins are registered (and thus accessible from the model), each loaded project starts with a clean
            (empty) set of registered plugins. Loading the project registers any plugins for newly loaded modules while this
            class is responsible for completing the set with appropriate previously registered plugins.
    """

    _registered_plugins: typing.Dict[str, typing.Type[plugins.Plugin]] = {}
    _dynamic_modules: typing.Set[str] = set()

    @classmethod
    def reset(cls) -> None:
        """
        Fully resets the ProjectLoader. For normal pytest-inmanta use this is not required (or even desired). It is used for
        resetting the singleton state in between distinct module tests for pytest-inmanta's own test suite.
        """
        cls._registered_plugins = {}
        cls._dynamic_modules = set()

    @classmethod
    def load(cls, project: module.Project) -> None:
        """
        Sets and loads the given project.
        """
        # unload dynamic modules before fetching currently registered plugins: they should not be included
        cls._unload_dynamic_modules()
        # add currently registered plugins to tracked plugins before loading the project
        cls._refresh_registered_plugins()
        # reset modules' state
        cls._reset_module_state()

        # For supported versions of core, don't clean up loaded modules between invocations to keep top-level imports valid
        signature_set: inspect.Signature = inspect.Signature.from_callable(
            module.Project.set
        )
        extra_kwargs_set = (
            {"clean": False} if "clean" in signature_set.parameters.keys() else {}
        )
        module.Project.set(project, **extra_kwargs_set)

        # deregister plugins
        plugins.PluginMeta.clear()

        # load the project
        if hasattr(project, "install_modules"):
            # more recent versions of core require explicit modules installation (ISO5+)
            project.install_modules()
        project.load()

        # complete the set of registered plugins from the previously registered ones
        cls._register_plugins(project)

    @classmethod
    def _refresh_registered_plugins(cls) -> None:
        """
        Refresh the tracked registered plugins. Should be called at least once between project loads.
        """
        cls._registered_plugins.update(plugins.PluginMeta.get_functions())

    @classmethod
    def _register_plugins(cls, project: module.Project) -> None:
        """
        Registers all plugin functions for a given project. For each of the project's loaded modules, reregisters any plugins
        that are not currently registered from the set of tracked plugins.
        """
        currently_registered_plugins: typing.Mapping[
            str, typing.Type[plugins.Plugin]
        ] = plugins.PluginMeta.get_functions()
        loaded_mod_ns_pattern: typing.Pattern[str] = re.compile(
            "(" + "|".join(re.escape(mod) for mod in project.modules.keys()) + ")::"
        )
        for fq_plugin_name, plugin in cls._registered_plugins.items():
            if (
                fq_plugin_name not in currently_registered_plugins
                and loaded_mod_ns_pattern.match(fq_plugin_name)
            ):
                plugins.PluginMeta.add_function(plugin)

    @classmethod
    def register_dynamic_module(cls, module_name: str) -> None:
        """
        Register a module as dynamic by name. Dynamic modules are forcefully reloaded on each project load.
        """
        cls._dynamic_modules.add(module_name)

    @classmethod
    def _unload_dynamic_modules(cls) -> None:
        """
        Unload all registered dynamic modules to force a reload on the next compile. Should be called at least once between
        project loads because it assumes that either a dynamic module is loaded by the currently active project or it was
        not loaded at all.
        """
        if not hasattr(module.Module, "unload"):
            # older versions of core (<6) don't support (and don't require) explicit module unloading
            return
        project: module.Project
        try:
            project = module.Project.get()
        except module.ProjectNotFoundException:
            # no project has been loaded yet, no need to unload any modules
            return
        for mod in cls._dynamic_modules:
            if mod in project.modules:
                project.modules[mod].unload()

    @classmethod
    def clear_dynamic_modules(cls) -> None:
        """
        Clear the set of registered dynamic modules, unloading them first.
        """
        cls._unload_dynamic_modules()
        cls._dynamic_modules = set()

    @classmethod
    def _reset_module_state(cls) -> None:
        """
        Resets any state kept on Python module objects associated with Inmanta modules by calling predefined cleanup functions.
        """
        for mod_name, mod in sys.modules.items():
            if mod_name.startswith("inmanta_plugins."):
                for func_name, func in mod.__dict__.items():
                    if func_name.startswith("inmanta_reset_state") and callable(func):
                        func()


def get_resources_matching(
    resources: "collections.abc.Iterable[Resource]",
    resource_type: str,
    should_filter_model_type: bool = False,
    **filter_args: object,
) -> Iterator[Resource]:
    """
    Return the resources that are matching the provided criteria. If none are provided, it will match every resource this
    function encounters.

    :param resources: The resources to filter on
    :param resource_type: The desired resource type
    :param should_filter_model_type: flag to have a stricter filtering -> make sure the entity type of the resource is matching
        the one provided in the arguments of the function.
    :param filter_args: Additional args to filter the resources
    """

    def apply_filter(resource: Resource) -> bool:
        for arg, value in filter_args.items():
            if not hasattr(resource, arg):
                return False

            if getattr(resource, arg) != value:
                return False

        return True

    for resource in resources:

        if not should_filter_model_type:
            if not resource.is_type(resource_type):
                continue
        else:
            if not resource.id.entity_type == resource_type:
                continue

        if not apply_filter(resource):
            continue

        yield resource


def check_serialization(resource: Resource) -> Resource:
    """Check if the resource is serializable"""
    serialized = json.loads(protocol.json_encode(resource.serialize()))
    return Resource.deserialize(serialized)


def get_resource(
    resources: "collections.abc.Iterable[Resource]",
    resource_type: str,
    should_filter_model_type: bool = False,
    **filter_args: object,
) -> typing.Optional[Resource]:
    """
    Get a resource of the given type and given filter on the resource attributes. If multiple resource match, the
    first one is returned. If none match, None is returned.

    :param resource_type: The exact type used in the model (no super types)
    """

    try:
        resource = next(
            get_resources_matching(
                resources, resource_type, should_filter_model_type, **filter_args
            )
        )
        resource = check_serialization(resource)
        return resource
    except StopIteration:
        return None


def get_one_resource(
    resources: "collections.abc.Iterable[Resource]",
    resource_type: str,
    **filter_args: object,
) -> typing.Optional[Resource]:
    """
    Get a resource of the given type and given filter on the resource attributes. This method makes sure that the
    `entity_type` matches the provided `resource_type`, unlike the `get_resource` function
    If multiple resource match, an assertion error is raised. If none match, None is returned.

    :param resources: The resources to filter on
    :param resource_type: The exact type used in the model (no super types)
    """
    resources = iter(
        get_resources_matching(
            resources,
            resource_type,
            should_filter_model_type=True,
            **filter_args,
        )
    )

    list_resources = []
    for resource in resources:
        resource = check_serialization(resource)
        list_resources.append(resource)

    # If we don't find anything matching these criteria, we should return `None`
    if len(list_resources) == 0:
        list_resources.append(None)

    assert len(list_resources) == 1, (
        "The filter should only match one resource, but it matches: "
        f"[{','.join(str(resource.id) for resource in list_resources)}]"
    )
    return list_resources[0]


class Result:
    def __init__(self, results: Dict[Resource, HandlerContext]) -> None:
        self.results = results

    def assert_all(self, status: ResourceState = ResourceState.deployed) -> None:
        for r, ct in self.results.items():
            assert (
                ct.status == status
            ), f"Resource {r.id} has status {ct.status.value}, expected {status.value}"

    def assert_has_no_changes(self) -> None:
        for r, ct in self.results.items():
            assert not bool(
                ct.changes
            ), f"Resource {r.id} has changes {ct.changes}, expected no changes"

    def assert_resources_have_purged(self) -> None:
        """
        Asserts that `purged` is in the changes. This is helpful to assert if the
        resources are to be created (`purged` set to True) or deleted (`purged` set to False)
        """
        for r, ct in self.results.items():
            assert ct.changes, f"Resource {r.id} has no changes, expected some changes"
            assert "purged" in ct.changes

    def get_contexts_for(
        self, resource_type: str, **filter_args: object
    ) -> Set[HandlerContext]:
        return {
            self.results[resource]
            for resource in get_resources_matching(
                self.results.keys(), resource_type, **filter_args
            )
        }

    def get_context_for(
        self, resource_type: str, **filter_args: object
    ) -> Optional[HandlerContext]:
        resources = list(
            get_resources_matching(self.results.keys(), resource_type, **filter_args)
        )
        if not resources:
            return None
        if len(resources) > 1:
            raise LookupError(
                "Multiple resources match this filter, if this is intentional, use get_contexts_for"
            )
        return self.results[resources[0]]

    def get_resource(
        self, resource_type: str, strict_mode: bool = False, **filter_args: object
    ) -> typing.Optional[Resource]:
        """
        Get a resource of the given type and given filter on the results attributes from a Result object.
        If multiple resource match, the first one is returned. If none match, None is returned.

        :param resource_type: The exact type used in the model (no super types)
        :param strict_mode: If we need to make additional assertion when retrieving the resource:
            - stricter filtering: matching the entity type of the resource
            - assert only one instance
        """
        if strict_mode:
            return self.get_one_resource(resource_type, **filter_args)
        else:
            return get_resource(
                self.results.keys(), resource_type, strict_mode, **filter_args
            )

    def get_one_resource(
        self, resource_type: str, **filter_args: object
    ) -> typing.Optional[Resource]:
        """
        Get a resource of the given type and given filter on the results attributes from a Result object.
        If multiple resource match, the first one is returned. If none match, None is returned.

        :param resource_type: The exact type used in the model (no super types)
        """
        return get_one_resource(self.results.keys(), resource_type, **filter_args)


DeployResult = Result
"""
Here for backwards compatibility reasons.
"""


@dataclass
class DeployResultCollection:
    first_dryrun: Result
    deploy: Result
    last_dryrun: Result


class Project:
    """
    This class provides a TestCase class for creating module unit tests. It uses the current module and loads required
    modules from the provided repositories. Additional repositories can be provided by setting the INMANTA_MODULE_REPO
    environment variable. Repositories are separated with spaces.
    """

    def __init__(
        self,
        project_dir: str,
        env_path: str,
        load_plugins: typing.Optional[bool] = True,
        no_strict_deps_check: typing.Optional[bool] = False,
    ) -> None:
        """
        :param project_dir: Directory containing the Inmanta project.
        :param env_path: The path to the venv to be used by the compiler.
        :param load_plugins: Load plugins iff this value is not None.
        """
        self._test_project_dir = project_dir
        self._env_path = env_path
        self.no_strict_deps_check = no_strict_deps_check
        self._stdout: typing.Optional[str] = None
        self._stderr: typing.Optional[str] = None
        self.types: typing.Optional[typing.Dict[str, inmanta.ast.Type]] = None
        self.version: typing.Optional[int] = None
        self.resources: ResourceDict = {}
        self._root_scope: typing.Optional[inmanta.ast.Namespace] = None
        self._exporter: typing.Optional[Exporter] = None
        self._blobs: typing.Dict[str, bytes] = {}
        self._facts: typing.Dict[ResourceIdStr, typing.Dict[str, typing.Any]] = (
            defaultdict(dict)
        )
        self._should_load_plugins: typing.Optional[bool] = load_plugins
        self._plugins: typing.Optional[typing.Dict[str, FunctionType]] = None
        self._load()
        self._capsys: typing.Optional["CaptureFixture"] = None
        self.ctx: typing.Optional[HandlerContext] = None
        self._handlers: typing.Set[ResourceHandler] = set()

        # The agent_map attribute can contain a mapping of agent name to io uri.
        # This can be used to overwrite the default behavior of the `get_handler`
        # method, and test a handler against a real remote host.
        # This attribute is part of the public interface of the `Project` class,
        # the developer can manipulate it directly, or populate it automatically using the
        # `populate_agent_map` method.
        self.agent_map: dict[str, str] = {}
        config.Config.load_config()

    def _set_sys_executable(self) -> None:
        """
        Store the python interpreter used by the compiler in sys.executable
        """
        python_name: str = os.path.basename(sys.executable)
        if sys.platform == "win32":
            compiler_executable = os.path.join(self._env_path, "Scripts", python_name)
        else:
            compiler_executable = os.path.join(self._env_path, "bin", python_name)

        sys.executable = compiler_executable

    def init(self, capsys: "CaptureFixture") -> None:
        self._stdout = None
        self._stderr = None
        self._capsys = capsys
        self.types = None
        self.version = None
        self.resources = {}
        self._root_scope = None
        self._exporter = None
        self._blobs = {}
        self._facts = defaultdict(dict)
        self.ctx = None
        self._handlers = set()
        self.agent_map = {}
        self._load()
        self._set_sys_executable()
        config.Config.load_config()

    def _create_project_and_load(self, model: str) -> module.Project:
        """
        This method does the following:
        * Add the given model file to the Inmanta project
        * Install the module dependencies
        * Load the project

        :param init: True iff the project should start from a clean slate. Ignored for older (<6) versions of core.
        :return: The newly created module.Project instance.
        """
        with open(os.path.join(self._test_project_dir, "main.cf"), "w+") as fd:
            fd.write(model)

        signature_init: inspect.Signature = inspect.Signature.from_callable(
            module.Project.__init__
        )
        # The venv_path parameter only exists on ISO5+

        extra_kwargs_init = (
            {"venv_path": self._env_path}
            if "venv_path" in signature_init.parameters.keys()
            else {}
        )

        if "strict_deps_check" in signature_init.parameters.keys():
            extra_kwargs_init["strict_deps_check"] = not self.no_strict_deps_check

        test_project = module.Project(
            self._test_project_dir,
            **extra_kwargs_init,
        )

        ProjectLoader.load(test_project)

        # refresh plugins
        if self._should_load_plugins is not None:
            self._plugins = self._load_plugins()
        return test_project

    def add_blob(self, key: str, content: bytes, allow_overwrite: bool = True) -> None:
        """
        Add a blob identified with the hash of the content as key
        """
        if isinstance(content, str):
            warnings.warn("received a string, but expect bytes", DeprecationWarning)
            content = content.encode("utf-8")
        if key in self._blobs and not allow_overwrite:
            raise Exception("Key %s already stored in blobs" % key)
        self._blobs[key] = content

    def stat_blob(self, key: str) -> bool:
        return key in self._blobs

    def get_blob(self, key: str) -> bytes:
        return self._blobs[key]

    def add_fact(self, resource_id: ResourceIdStr, name: str, value: object) -> None:
        self._facts[resource_id][name] = value

    def get_handler(self, resource: Resource, run_as_root: bool) -> ResourceHandler:
        # TODO: if user is root, do not use remoting
        c = cache.AgentCache()
        if resource.id.agent_name in self.agent_map:
            # If the agent is in the agent map, we keep its uri, this allows
            # us to test remote agent (with respect to the configuration target)
            # + remote io (with respect to the agent process) scenarios
            agent = MockAgent(self.agent_map[resource.id.agent_name])
        elif run_as_root:
            agent = MockAgent("ssh://root@localhost")
        else:
            agent = MockAgent("local:")

        def setup_handler(cache: AgentCache, provider: HandlerAPI) -> ResourceHandler:
            try:
                provider.set_cache(cache)
                provider.get_file = lambda x: self.get_blob(x)  # type: ignore
                provider.stat_file = lambda x: self.stat_blob(x)  # type: ignore
                provider.upload_file = lambda x, y: self.add_blob(x, y)  # type: ignore
                provider.run_sync = ioloop.IOLoop.current().run_sync  # type: ignore
                provider._client = MockClient()
                self._handlers.add(provider)
                return provider
            except Exception as e:
                raise e

        if hasattr(c, "open_version"):
            c.open_version(resource.id.version)
            p = handler.Commander.get_provider(c, agent, resource)  # type: ignore
        else:
            # ISO8 and later no longer have the cache argument
            p = handler.Commander.get_provider(agent, resource)  # type: ignore

        return setup_handler(c, p)

    def finalize_context(self, ctx: handler.HandlerContext) -> None:
        # ensure logs can be serialized
        protocol.json_encode({"message": ctx.logs})

    def get_resource(
        self, resource_type: str, strict_mode: bool = False, **filter_args: object
    ) -> typing.Optional[Resource]:
        """
        Get a resource of the given type and given filter on the resource attributes. If multiple resource match, the
        first one is returned. If none match, None is returned.

        :param resource_type: The exact type used in the model (no super types)
        :param strict_mode: If we need to make additional assertion when retrieving the resource:
            - stricter filtering: matching the entity type of the resource
            - assert only one instance
        """
        if strict_mode:
            return self.get_one_resource(resource_type, **filter_args)
        else:
            return get_resource(self.resources.values(), resource_type, **filter_args)

    def get_one_resource(
        self, resource_type: str, **filter_args: object
    ) -> typing.Optional[Resource]:
        """
        Get a resource of the given type and given filter on the resource attributes. If multiple resource match, the
        first one is returned. If none match, None is returned.

        :param resource_type: The exact type used in the model (no super types)
        """
        return get_one_resource(self.resources.values(), resource_type, **filter_args)

    def resolve_references(
        self, resource: Resource, ctx: LoggerABC | None = None
    ) -> None:
        """
        Resolve all references in the resource
        """
        if hasattr(resource, "resolve_all_references"):
            # Pre ISO 8.1 versions don't have this
            if ctx is None:
                ctx = PythonLogger(LOGGER)
            resource.resolve_all_references(ctx)

    def deploy(
        self, resource: Resource, dry_run: bool = False, run_as_root: bool = False
    ) -> HandlerContext:
        """
        Deploy the given resource with a handler
        """
        assert resource is not None

        h = self.get_handler(resource, run_as_root)

        assert h is not None

        ctx = handler.HandlerContext(resource, dry_run=dry_run)
        try:
            self.resolve_references(resource, ctx)
        except Exception as e:
            # Resolver failure
            ctx.set_resource_state(const.HandlerResourceState.failed)
            ctx.exception(
                "An error occurred during deployment of %(resource_id)s (exception: %(exception)s",
                resource_id=str(resource.id),
                exception=repr(e),
            )
            return ctx
        # Normal execution
        h.execute(ctx, resource, dry_run)
        self.finalize_context(ctx)
        self.ctx = ctx
        self.finalize_handler(h)
        return ctx

    def deploy_all(
        self, run_as_root: bool = False, exclude_all: List[str] = ["std::AgentConfig"]
    ) -> Result:
        """
        Deploy all resources, in the correct order.

        This method handles skips and failures like the normal orchestrator.

        However, it can not handle Undefined resources.

        :param exclude_all: list of resource types to exclude from the deploy
        """
        # clear context, just to avoid confusion
        self.ctx = None

        def build_handler_and_context(
            resource: Resource,
        ) -> Tuple[Resource, ResourceHandler, HandlerContext]:
            h = self.get_handler(resource, run_as_root)
            assert h is not None
            ctx = HandlerContext(resource)
            return resource, h, ctx

        all_contexts = {
            str(rid): build_handler_and_context(resource)
            for rid, resource in self.resources.items()
            if not any(resource.is_type(extype) for extype in exclude_all)
        }

        todo: List[str] = sorted(list(all_contexts.keys()))
        order: List[str] = []

        def topo_sort(doing: List[str], current: str):
            # to be replace with graphlib.TopologicalSorter when we drop python 3.6 support
            # Will not win a beauty contest, but it is stable and works
            if current not in todo:
                return
            if current in doing:
                raise Exception(f"Cycle detected: {doing}")

            todo.remove(current)

            new_doing = doing + [current]
            for req in all_contexts[current][0].requires:
                topo_sort(new_doing, str(req))
            order.append(current)

        while todo:
            topo_sort([], todo[0])

        for rid in order:
            resource, h, ctx = all_contexts[rid]
            skip = any(
                all_contexts[str(dependency)][2].status != ResourceState.deployed
                for dependency in resource.requires
                if str(dependency) in all_contexts
            )
            if skip:
                LOGGER.debug("Skipping %s", resource.id)
                ctx.set_status(ResourceState.skipped)
            else:
                LOGGER.debug("Start executing %s", resource.id)
                try:
                    self.resolve_references(resource, ctx)
                except Exception as e:
                    # Resolver failure
                    ctx.set_resource_state(const.HandlerResourceState.failed)
                    ctx.exception(
                        "An error occurred during deployment of %(resource_id)s (exception: %(exception)s",
                        resource_id=str(resource.id),
                        exception=repr(e),
                    )
                else:
                    # Normal execution
                    h.execute(ctx, resource)
                LOGGER.debug("Done executing %s", resource.id)
            self.finalize_context(ctx)
            self.finalize_handler(h)

        return Result({r: ctx for r, _, ctx in all_contexts.values()})

    def dryrun(self, resource: Resource, run_as_root: bool = False) -> HandlerContext:
        return self.deploy(resource, True, run_as_root)

    def deploy_resource(
        self,
        resource_type: str,
        status: const.ResourceState = const.ResourceState.deployed,
        run_as_root: bool = False,
        change: const.Change = None,
        **filter_args: object,
    ) -> Resource:
        """
        Deploy a resource of the given type, that matches the filter and assert the outcome

        :param resource_type: the type of resource to deploy
        :param filter_args: a set of kwargs, the resource must have all matching attributes set to the given values
        :param run_as_root: run the handler as root or not
        :param status: the expected status of the deployment
        :param change: the expected change performed by the handler

        :return: the resource
        """
        res = self.get_resource(resource_type, **filter_args)
        assert res is not None, "No resource found of given type and filter args"

        ctx = self.deploy(res, run_as_root)
        if ctx.status != status:
            print("Deploy did not result in correct status")
            print("Requested changes: ", ctx._changes)
            for log in ctx.logs:
                print("Log: ", log._data["msg"])
                print(
                    "Kwargs: ",
                    [
                        "%s: %s" % (k, v)
                        for k, v in log._data["kwargs"].items()
                        if k != "traceback"
                    ],
                )
                if "traceback" in log._data["kwargs"]:
                    print("Traceback:\n", log._data["kwargs"]["traceback"])

        assert ctx.status == status
        if change is not None:
            assert ctx._change == change
        self.finalize_context(ctx)
        return res

    def dryrun_resource(
        self,
        resource_type: str,
        status: const.ResourceState = const.ResourceState.dry,
        run_as_root: bool = False,
        **filter_args: object,
    ) -> typing.Dict[str, AttributeStateChange]:
        """
        Run a dryrun for a specific resource.

        :param resource_type: the type of resource to run, as a fully qualified inmanta type (e.g. `unittest::Resource`),
            see :py:meth:`get_resource`
        :param status: the expected result status
            (for dryrun the success status is :py:attr:`inmanta.const.ResourceState.dry`)
        :param run_as_root: run the mock agent as root
        :param filter_args: filters for selecting the resource, see :py:meth:`get_resource`
        """
        res = self.get_resource(resource_type, **filter_args)
        assert res is not None, "No resource found of given type and filter args"

        ctx = self.dryrun(res, run_as_root)
        assert ctx.status == status
        return ctx.changes

    def dryrun_all(self, run_as_root: bool = False) -> Result:
        """
        Runs a dryrun for every resource.
        :param run_as_root: run the mock agent as root
        """
        return Result(
            {
                r: self.dryrun(r, run_as_root=run_as_root)
                for r in self.resources.values()
            }
        )

    def dryrun_and_deploy_all(
        self, run_as_root: bool = False, assert_create_or_delete: bool = False
    ) -> DeployResultCollection:
        """
        Runs a dryrun, followed by a deploy and a final dryrun for every resource and asserts the expected behaviour.
        :param run_as_root: run the mock agent as root
        :param assert_create_or_delete: assert that every resource will either be created or deleted.
        """
        first_dryrun = self.dryrun_all(run_as_root=run_as_root)
        first_dryrun.assert_all(const.ResourceState.dry)

        if assert_create_or_delete:
            first_dryrun.assert_resources_have_purged()

        deploy = self.deploy_all(run_as_root=run_as_root)
        deploy.assert_all(const.ResourceState.deployed)

        last_dryrun = self.dryrun_all(run_as_root=run_as_root)
        last_dryrun.assert_all(const.ResourceState.dry)
        last_dryrun.assert_has_no_changes()

        return DeployResultCollection(
            first_dryrun=first_dryrun, deploy=deploy, last_dryrun=last_dryrun
        )

    def create_module(self, name: str, initcf: str = "", initpy: str = "") -> None:
        module_dir = os.path.join(self._test_project_dir, "libs", name)
        os.mkdir(module_dir)
        os.mkdir(os.path.join(module_dir, "model"))
        os.mkdir(os.path.join(module_dir, "files"))
        os.mkdir(os.path.join(module_dir, "templates"))
        os.mkdir(os.path.join(module_dir, "plugins"))

        with open(os.path.join(module_dir, "model", "_init.cf"), "w+") as fd:
            fd.write(initcf)

        with open(os.path.join(module_dir, "plugins", "__init__.py"), "w+") as fd:
            fd.write(initpy)

        with open(os.path.join(module_dir, "module.yml"), "w+") as fd:
            fd.write(
                f"""name: {name}
version: 0.1
license: Test License
            """
            )

        ProjectLoader.register_dynamic_module(name)

    def _load(self) -> None:
        """
        Load the current module and compile an otherwise empty project
        """
        mod: module.Module
        mod, _ = get_module()
        self._create_project_and_load(model=f"import {mod.name}")

    def populate_agent_map(self) -> None:
        """
        Populate the agent map attribute based on the agent config resources present in the
        desired state.
        This method can only be called after a compile.
        It doesn't cleanup the agent map from existing entries, but will overwrite existing
        ones if a newer version of the agent config is part of the desired state.
        """
        for resource_id, resource in self.resources.items():
            if resource_id.entity_type != "std::AgentConfig":
                # This is not an agent config
                continue

            # Save the uri for this agent name
            self.agent_map[resource.agentname] = resource.uri

    def compile(self, main: str, export: bool = False, no_dedent: bool = True) -> None:
        """
        Compile the configuration model in main. This method will load all required modules.

        :param main: The model to compile
        :param export: Whether the model should be exported after the compile
        :param no_dedent: Don't remove additional indentation in the model
        """

        # logging model with line numbers
        def enumerate_model(model: str):
            lines = model.split("\n")
            leading_zeros = math.floor(math.log(len(lines), 10)) + 1
            line_numbers_model = "\n".join(
                [
                    f"{str(number).zfill(leading_zeros)}    {line}"
                    for number, line in enumerate(lines, start=1)
                ]
            )
            return line_numbers_model

        # Dedent the input format
        model = dedent(main.strip("\n")) if not no_dedent else main
        LOGGER.debug(f"Compiling model:\n{enumerate_model(model)}")
        self._create_project_and_load(model)

        # flush io capture buffer
        self._capsys.readouterr()

        (types, scopes) = compiler.do_compile(refs={"facts": self._facts})

        exporter = Exporter()

        version, resources = exporter.run(types, scopes, no_commit=not export)

        for key, blob in exporter._file_store.items():
            self.add_blob(key, blob)

        for cls_name, value in inmanta.resources.resource._resources.items():
            name_id_attribute = value[1]["name"]
            if name_id_attribute == "id":
                warnings.warn(
                    "In one of the next major releases of inmanta-core it will not be possible "
                    f"anymore to use an id_attribute called id for {cls_name}",
                    DeprecationWarning,
                )

        # Fix the resource serialization (fully serialize them)
        new_resources = {}
        for resource_id, resource in resources.items():
            new_resource = inmanta.resources.Resource.deserialize(
                json.loads(inmanta.protocol.common.json_encode(resource.serialize()))
            )
            new_resource.model = resource.model
            new_resources[resource_id] = new_resource

        self._root_scope = scopes
        self.version = version
        self.resources = new_resources
        self.types = types
        self._exporter = exporter

        captured = self._capsys.readouterr()

        self._stdout = captured.out
        self._stderr = captured.err

    def deploy_latest_version(self, full_deploy: bool = False) -> None:
        """Release and push the latest version to the server (uses the current configuration, either with a fixture or
        set by the test.
        """
        if self.version is None:
            raise Exception("Run project.compile first")
        conn = protocol.SyncClient("compiler")
        LOGGER.info("Triggering deploy for version %d" % self.version)
        tid = cfg_env.get()
        agent_trigger_method = const.AgentTriggerMethod.get_agent_trigger_method(
            full_deploy
        )
        conn.release_version(tid, self.version, True, agent_trigger_method)

    def get_last_context(self) -> typing.Optional[HandlerContext]:
        return self.ctx

    def get_last_logs(self) -> typing.Optional[typing.List[LogLine]]:
        if self.ctx:
            return self.ctx.logs
        return None

    def get_stdout(self) -> typing.Optional[str]:
        return self._stdout

    def get_stderr(self) -> typing.Optional[str]:
        return self._stderr

    def get_root_scope(self) -> typing.Optional[inmanta.ast.Namespace]:
        return self._root_scope

    def add_mock_file(self, subdir: str, name: str, content: str) -> None:
        """
        This method can be used to register mock templates or files in the virtual "unittest" module.
        """
        dir_name = os.path.join(self._test_project_dir, "libs", "unittest", subdir)
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)

        with open(os.path.join(dir_name, name), "w+") as fd:
            fd.write(content)

        ProjectLoader.register_dynamic_module("unittest")

    def _load_plugins(self) -> typing.Dict[str, FunctionType]:
        mod: module.Module
        mod, _ = get_module()
        submodules: typing.Optional[typing.Dict[str, ModuleType]] = (
            InmantaPluginsImporter(self).get_submodules(mod.name)
        )
        return (
            {}
            if submodules is None
            else {
                k: v
                for submod in submodules.values()
                for k, v in submod.__dict__.items()
                if isinstance(v, FunctionType)
            }
        )

    def get_plugin_function(self, function_name: str) -> FunctionType:
        if self._plugins is None:
            raise Exception(
                "Plugins not loaded, perhaps you should use the `project` fixture or"
                " initialize the Project with load_plugins == True"
            )
        if function_name not in self._plugins:
            raise Exception(f"Plugin function with name {function_name} not found")
        return self._plugins[function_name]

    def get_plugins(self) -> typing.Dict[str, FunctionType]:
        if self._plugins is None:
            raise Exception(
                "Plugins not loaded, perhaps you should use the `project` fixture or"
                " initialize the Project with load_plugins == True"
            )
        return dict(self._plugins)

    def get_instances(self, fortype: str = "std::Entity") -> typing.List[DynamicProxy]:
        if self.types is None:
            raise Exception("No compile has been done")
        if fortype not in self.types:
            raise Exception(f"No entities of type {fortype} found in the model")

        # extract all objects of a specific type from the compiler
        allof = self.types[fortype].get_all_instances()
        # wrap in DynamicProxy to hide internal compiler structure
        # and get inmanta objects as if they were python objects
        return [DynamicProxy.return_value(port) for port in allof]

    def unittest_resource_exists(self, name: str) -> bool:
        """
        Check if a unittest resource with name exists or not
        """
        return name in DATA

    def unittest_resource_get(
        self, name: str
    ) -> typing.Dict[str, typing.Union[str, bool, float, int]]:
        """
        Get the state of the unittest resource
        """
        return DATA[name]

    def unittest_resource_set(
        self, name: str, **kwargs: typing.Union[str, bool, float, int]
    ) -> None:
        """
        Change a value of the unittest resource
        """
        DATA[name].update(kwargs)

    def check_serialization(self, resource: Resource) -> Resource:
        return check_serialization(resource)

    def clean(self) -> None:
        shutil.rmtree(os.path.join(self._test_project_dir, "libs", "unittest"))
        self.finalize_all_handlers()
        self.create_module(
            "unittest",
            initcf=get_module_data("init.cf"),
            initpy=get_module_data("init.py"),
        )
        ProjectLoader.clear_dynamic_modules()
        os.chdir(CURDIR)
        sys.executable = SYS_EXECUTABLE

    def finalize_handler(self, handler: ResourceHandler) -> None:
        handler.cache.close()

    def finalize_all_handlers(self) -> None:
        for handler_instance in self._handlers:
            self.finalize_handler(handler_instance)

    def deploy_resource_v2(
        self,
        resource_type: str,
        run_as_root: bool = False,
        dry_run: bool = False,
        expected_status: Optional[const.ResourceState] = DEFAULT,
        **filter_args: object,
    ) -> "DeployResultV2":
        """
        Deploy a resource of the given type, that matches the filter and assert the outcome

        :param resource_type: the type of resource to deploy
        :param filter_args: a set of kwargs, the resource must have all matching attributes set to the given values
        :param run_as_root: run the handler as root or not
        :param dry_run: only perform dryrun
        :param status: expected status after deploy,
            set to None to not check,
            for deploy defaults to deployed
            for dryrun defaults to dry
        """
        if expected_status == DEFAULT:
            expected_status = (
                const.ResourceState.deployed if not dry_run else const.ResourceState.dry
            )

        resource = self.get_resource(resource_type, **filter_args)
        assert resource is not None, "No resource found of given type and filter args"

        h = self.get_handler(resource, run_as_root)
        assert h is not None

        ctx = handler.HandlerContext(resource, dry_run=dry_run)
        try:
            self.resolve_references(resource, ctx)
        except Exception as e:
            # Resolver failure
            ctx.set_resource_state(const.HandlerResourceState.failed)
            ctx.exception(
                "An error occurred during deployment of %(resource_id)s (exception: %(exception)s",
                resource_id=str(resource.id),
                exception=repr(e),
            )
        else:
            # Normal execution
            h.execute(ctx, resource, dry_run)
        self.finalize_context(ctx)
        self.finalize_handler(h)

        out = DeployResultV2(resource=resource, ctx=ctx, handler=h)
        if expected_status is not None:
            out.assert_status(expected_status)

        return out

    def dryrun_resource_v2(
        self,
        resource_type: str,
        run_as_root: bool = False,
        expected_status: Optional[const.ResourceState] = DEFAULT,
        **filter_args: object,
    ) -> "DeployResultV2":
        return self.deploy_resource_v2(
            resource_type, run_as_root, True, expected_status, **filter_args
        )


@dataclass
class DeployResultV2:
    ctx: HandlerContext
    handler: ResourceHandler
    resource: Resource

    # status
    def assert_status(
        self,
        status: const.ResourceState = const.ResourceState.deployed,
        change: const.Change = None,
    ) -> None:
        ctx = self.ctx
        if ctx.status != status:
            loglines = [
                "Deploy did not result in correct status",
                f"Requested changes: {ctx._changes}" f"Outputting resource logs",
            ]

            for log in ctx.logs:
                loglines.append(f"Log: {log._data['msg']}")
                formattedkwargs = [
                    "%s: %s" % (k, v)
                    for k, v in log._data["kwargs"].items()
                    if k != "traceback"
                ]
                if formattedkwargs:
                    loglines.append("\tKwargs: " + ",".join(formattedkwargs))
                if "traceback" in log._data["kwargs"]:
                    loglines.append(f"\tTraceback: {log._data['kwargs']['traceback']}")

        assert ctx.status == status, "\n\t".join(loglines)
        if change is not None:
            assert ctx._change == change
        self.assert_consistent_status()

    # Discovery
    @property
    def discovered_resources(self) -> list[object]:
        return self.handler._client.discovered_resources

    # Logs
    @property
    def logs(self) -> list[LogLine]:
        return self.ctx.logs

    def assert_has_logline(self, matches: str) -> LogLine:
        """
         Assert the handler logged a log line matching the pattern

        :return: that logline
        """
        pattern = re.compile(matches)
        for logline in self.logs:
            if pattern.search(logline.msg):
                return logline
        assert False, f"No line found matching {pattern}"

    # changes
    @property
    def changes(self) -> Dict[str, AttributeStateChange]:
        return self.ctx.changes

    def assert_no_changes(self) -> None:
        """Assert that the diff produced no changes"""
        assert not self.changes

    def assert_consistent_status(self) -> None:
        """Make sure we report change and doing changes consistently"""
        if self.ctx.status != const.ResourceState.deployed:
            return

        if bool(self.ctx.changes):
            assert (
                self.ctx.change != const.Change.nochange
            ), f"""Inconsistent handler state:
    the handler reported it was deployed successful,
    that it had {len(self.ctx.changes)} changes when doing the diff
    and performed no change during deploy.

    Perhaps you forgot to call ctx.set_created(), ctx.set_updated() or ctx.set_deleted()?
"""
        else:
            assert self.ctx.change == const.Change.nochange


@pytest.fixture(scope="function")
def inmanta_state_dir(tmpdir_factory: "TempdirFactory") -> Iterator[str]:
    """
    This fixture can be overridden in the conftest of any individual project
    in order to set the Inmanta state directory at the desired level.
    """
    inmanta_state_dir = tmpdir_factory.mktemp("inmanta_state_dir")
    yield str(inmanta_state_dir)
    inmanta_state_dir.remove()


@pytest.fixture
def set_inmanta_state_dir(inmanta_state_dir: str) -> None:
    inmanta_config.state_dir.set(inmanta_state_dir)
