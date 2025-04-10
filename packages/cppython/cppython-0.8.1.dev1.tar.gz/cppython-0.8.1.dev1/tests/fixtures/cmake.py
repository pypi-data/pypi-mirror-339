"""Fixtures for the cmake plugin"""

from pathlib import Path
from typing import cast

import pytest

from cppython.plugins.cmake.schema import CMakeConfiguration
from cppython.test.schema import Variant, Variants


def _cmake_data_list() -> Variants[CMakeConfiguration]:
    """Creates a list of mocked configuration types

    Returns:
        A list of variants to test
    """
    data = Variants[CMakeConfiguration]()

    # Default
    default = CMakeConfiguration(configuration_name='default')
    default_variant = Variant[CMakeConfiguration](configuration=default)

    # Non-root preset file
    config = CMakeConfiguration(preset_file=Path('inner/CMakePresets.json'), configuration_name='default')
    config_variant = Variant[CMakeConfiguration](configuration=config, directory=Path('cmake/non-root'))

    data.variants.append(default_variant)
    data.variants.append(config_variant)

    return data


@pytest.fixture(
    name='cmake_data',
    scope='session',
    params=_cmake_data_list(),
)
def fixture_cmake_data(request: pytest.FixtureRequest) -> Variant[CMakeConfiguration]:
    """A fixture to provide a list of configuration types

    Args:
        request: Parameterization list

    Returns:
        A configuration type instance
    """
    return cast(Variant[CMakeConfiguration], request.param)
