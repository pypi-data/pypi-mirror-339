"""Field extractors for enums and data classes.

Used in tests and config management.
"""

from dataclasses import fields
from enum import Enum


def enum_field_names(c: type) -> list[str]:
    """List of all names of variants of an enum."""
    assert issubclass(c, Enum)
    return [v.name for v in c]


def dataclass_field_names(c: type) -> list[str]:
    """List of all names of fields of a dataclass."""
    return [f.name for f in fields(c)]
