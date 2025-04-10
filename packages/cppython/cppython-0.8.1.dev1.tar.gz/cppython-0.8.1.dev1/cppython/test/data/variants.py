"""Data definitions"""

from pathlib import Path

from cppython.core.schema import (
    CPPythonGlobalConfiguration,
    CPPythonLocalConfiguration,
    PEP621Configuration,
    ProjectConfiguration,
)
from cppython.test.schema import Variant, Variants


def _pep621_configuration_list() -> Variants[PEP621Configuration]:
    """Creates a list of mocked configuration types

    Returns:
        A list of variants to test
    """
    data = Variants[PEP621Configuration]()

    # Default
    default = PEP621Configuration(name='default-test', version='1.0.0')
    default_variant = Variant[PEP621Configuration](configuration=default)

    data.variants.append(default_variant)

    return data


def _cppython_local_configuration_list() -> Variants[CPPythonLocalConfiguration]:
    """Mocked list of local configuration data

    Returns:
        A list of variants to test
    """
    data = Variants[CPPythonLocalConfiguration]()

    # Default
    default = CPPythonLocalConfiguration()
    default_variant = Variant[CPPythonLocalConfiguration](configuration=default)

    data.variants.append(default_variant)

    return data


def _cppython_global_configuration_list() -> Variants[CPPythonGlobalConfiguration]:
    """Mocked list of global configuration data

    Returns:
        A list of variants to test
    """
    data = Variants[CPPythonGlobalConfiguration]()

    # Default
    default = CPPythonGlobalConfiguration()
    default_variant = Variant[CPPythonGlobalConfiguration](configuration=default)

    # Check off
    check_off_data = {'current-check': False}
    check_off = CPPythonGlobalConfiguration(**check_off_data)
    check_off_variant = Variant[CPPythonGlobalConfiguration](configuration=check_off)

    data.variants.append(default_variant)
    data.variants.append(check_off_variant)

    return data


def _project_configuration_list() -> Variants[ProjectConfiguration]:
    """Mocked list of project configuration data

    Returns:
        A list of variants to test
    """
    data = Variants[ProjectConfiguration]()

    # NOTE: pyproject_file will be overridden by fixture

    # Default
    default = ProjectConfiguration(project_root=Path(), version='0.1.0')
    default_variant = Variant[ProjectConfiguration](configuration=default)

    data.variants.append(default_variant)

    return data


pep621_variants = _pep621_configuration_list()
cppython_local_variants = _cppython_local_configuration_list()
cppython_global_variants = _cppython_global_configuration_list()
project_variants = _project_configuration_list()
