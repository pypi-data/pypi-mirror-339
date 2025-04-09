# v 3.2.0 (2025-04-09)
Changes in this release:
- Add support for references
- Format code using black 25.1.0
- Make sure to use pydantic v2+ methods
- Fix configuration of temporary state dir with the project fixture
- Remove reference to deprecated module install command

# v 3.1.0 (2024-10-10)
Changes in this release:
- Allow to use relative path for PathTestParameter
- Add compatibility with ISO8 AgentCache

# v 3.0.0 (2024-08-19)
Changes in this release:
- Remove io support to be compatible with ISO8
- Add strict mode in `get_resource` method to  the `project` fixture and `Result` object (by default set to `False`). 

## Updating
- All uses of the `get_resource` method should be replaced with the `get_one_resource` method. It has improved type matching and raises an exception when multiple matches are present.

# v 2.10.0 (2024-07-05)
Changes in this release:
- Add support for custom `agent_map` enabling testing or remote io scenarios.
- Fix resource serialization (#437)
- Fix new agent api in inmanta.agent.executor.AgentInstance (ISO8)
- Add `get_one_resource` method to the `project` fixture and `Result` object.

# v 2.9.0 (2023-11-29)
Changes in this release:
- Add support for more values (yes, 1) and (no, 0) for boolean options
- Add `deploy_resouce_v2` endpoint
- Add support for unmanaged resources
- Adds a new resource entity that raises an IgnoreResourceException when buildings its id
- Add support for ISO7. 
- Add `--pip-pre`, `--pip-use-system-config` and `--pip-index-url`

# v 2.8.0 (2023-08-03)
Changes in this release:
- Log a warning when the id_attribute of a resource is called id.
- Ignore `__pycache__` dirs when copying the current module to the test project dir
- Introduce `--pip-index-url` option to set corresponding project config section for inmanta-core 9.0.
- Dropped nonexistent option from the README

# v 2.7.0 (2023-02-23)
Changes in this release:
- Introduce `project_metadata` fixture to allow modifying the `project.yml` file for the project created by the project fixture.

# v 2.6.0 (2023-02-02)
Changes in this release:
- Add `dryrun_all` method to  the `project` fixture. Does a dryrun on every resource of a project. Also does some sanity checks.
- Add `dryrun_and_deploy_all` method to the `project` fixture. Dryruns, deploys and does a final dryrun on every resource of a project. Also does some sanity checks.
# v 2.5.0 (2023-01-20)
Changes in this release:
- Fix bug where the temporary directory used to store the Inmanta project is not cleaned up when an exception occurs in the setup stage of the project\_factory fixture.

# v 2.4.0 (2022-09-07)
Changes in this release:
- Add fixture to change the Inmanta state dir to a writable location for the current user.
- Add a new '--no-strict-deps-check' option to run pytest-inmanta using the legacy check on requirements.
By default the new strict check of core will be used.

# v 2.3.3 (2022-05-18)
Changes in this release:
 - Fix enum test parameters registered after pytest has loaded pytest-inmanta plugin.

# v 2.3.2 (2022-05-17)
Changes in this release:
 - Allow other plugins to register test parameters after pytest has loaded pytest-inmanta plugin.

# v 2.3.1 (2022-05-16)
Changes in this release:
 - Fixed test parameter framework for boolean options.

# v 2.3.0 (2022-05-13)
Changes in this release:
- Added test parameter framework (#288).
- Some options have been deprecated:
  -  `--no_load_plugins` in favor of `--no-load-plugins` (and `INMANTA_TEST_NO_LOAD_PLUGINS` in favor of `INMANTA_NO_LOAD_PLUGINS`)
  -  `--module_repo` in favor of `--module-repo`
  -  `--install_mode` in favor of `--install-mode`

# v 2.2.0 (2022-04-26)
Changes in this release:
- The `project` fixture now makes `sys.executable` point to the compiler's executable

# v 2.1.0 (2022-03-30)
Changes in this release:
- Fix bug where the `project` fixture doesn't reset the current working directory in the cleanup stage.
- Add deploy_all method to the `project` fixture

# v 2.0.0 (2022-01-24)
Changes in this release:
- Added support for testing v2 modules.
- Extended to be compatible with `inmanta-core>=6`
- Added support for custom `inmanta_reset_state` method to clean up stateful modules between compiles
- Ensure that projects are compiled using a separate venv.
- Fixed typing issue for `filter_args` in different method of the Project class.

## Breaking changes
- pytest-inmanta now keeps `inmanta_plugins` submodules alive across compiles. As a result, stateful modules must implement
    custom state cleanup logic as described in the README.

# v 1.6.2 (2021-08-17)
Changes in this release:
- Fixed issue with project fixture related to cleanup assumptions causing failures for `inmanta-core>=5.1.2.dev`

# v 1.6.1 (2021-06-29)
Changes in this release:
- Fixed an invalid import from inmanta-core (inmanta/inmanta-core#3074)

# v 1.6.0 (2021-06-18)
Changes in this release:
- Added the ability to assert the expected 'change' of a deploy
- Compiled models are logged (debug level), with line numbers (#199)
- Export mypy types

# v 1.5.0 (2021-03-26)
Changes in this release:
- Remove dependency on the inmanta package

# V 1.4.0 (20-10-12)
Changes in this release:
- Added meaningful error message when --venv points to a non-existing directory (#62)
- Ensure that cache is closed completely (#57)
- Fix incompatibility with pytest 6.0.0
- Fixed plugin loading compatibility with compiler's import mechanism (#46, #49)
- Added `inmanta_plugins` fixture to make abstraction of required module reloading when the compiler project is reset (related to #49)
- Added deprecation warning for `project_no_plugins` fixture in favor of `INMANTA_TEST_NO_LOAD_PLUGINS` environment variable (#66)
- Added resource unittest::IgnoreResource.
- Improve documentation of options (#67)

# V 1.3.0
Changes in this release:
- Added INMANTA_TEST_NO_LOAD_PLUGINS environment variable as workaround for inmanta/pytest-inmanta#49

# V 1.2.0
Changes in this release:
- Fixed status field on dryrun_resource (#53)
- Fixed error when running tests for module that imports other modules from its plugins
- Added project_no_plugins fixture as workaround for plugins being loaded multiple times (inmanta/pytest-inmanta#49)

# V 1.1.0
Changes in this release:
- Added --use-module-in-place option (#30)
- Added support to test regular functions and classes (#37)
- Close handler caches on cleanup (#42)

# V 1.0.0
Changes in this release:
- Added support to get logs from handler (#35)
- Added support to specify multiple --repo-path options (#38)
- Added --install_mode option

# V 0.10.0
Changes in this release:

# V 0.9.0
Changes in this release:

## Added
- Added support to retrieve scopes in project fixture.
- Test the serialization/deserialization of resources.

## Fixed
- Ensure that the project fixture doesn't leak any data across test cases.

# V 0.8.0
Changes in this release:
- Add suport for skip and fail through data global

# V 0.7.2
Changes in this release:
- Prevent IOError when using remote IO

# V 0.7.1
Changes in this release:
- Fix packaging bug

# V 0.7.0
Changes in this release:
- Various bugfixes
- Use yaml.safe_load() instead of yaml.load()
- Documentation on how to test plugins
- Add unittest handlers

# V 0.6.0
Changes in this release:
- added log serialization to deploy, to better mimic agent behavior
- added dryrun
