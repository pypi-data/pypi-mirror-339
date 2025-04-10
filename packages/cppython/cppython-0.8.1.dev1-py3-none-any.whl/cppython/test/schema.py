"""Data schemas for plugin testing"""

from pathlib import Path
from typing import Annotated

from pydantic import Field

from cppython.core.schema import CPPythonModel


class Variant[T: CPPythonModel](CPPythonModel):
    """A configuration variant for a schema type"""

    configuration: Annotated[T, Field(description='The configuration data')]
    directory: Annotated[
        Path | None,
        Field(description='The directory to mount alongside the configuration. `tests/build/<directory>`'),
    ] = None


class Variants[T: CPPythonModel](CPPythonModel):
    """A group of variants"""

    variants: Annotated[list[Variant[T]], Field(description='Data variants')] = []
