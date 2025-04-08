"""Tests for hvlbuzz.config.config."""

from dataclasses import dataclass
from enum import Enum

from hvlbuzz.config.config import extract_attribute_doc_strings
from hvlbuzz.config.field_names import dataclass_field_names, enum_field_names


class E(Enum):
    """Example enum."""

    variant = 1
    """Some variant."""
    other_variant = 2
    """A variant with a name ending with the name of the previous variant."""


@dataclass
class D:
    """Example dataclass."""

    example_field: int
    """Some field."""
    other_example_field: bool
    """Other field.

    The name is ending with the name of the previous field."""


def test_extract_attribute_doc_strings_works_for_enums() -> None:
    """Check enums."""
    doc_strings = list(extract_attribute_doc_strings(E, enum_field_names))
    expected_doc_strings = [
        ("variant", "Some variant."),
        ("other_variant", "A variant with a name ending with the name of the previous variant."),
    ]
    assert doc_strings == expected_doc_strings


def test_extract_attribute_doc_strings_works_for_dataclasses() -> None:
    """Check dataclasses."""
    doc_strings = list(extract_attribute_doc_strings(D, dataclass_field_names))
    expected_doc_strings = [
        ("example_field", "Some field."),
        (
            "other_example_field",
            "Other field.\n\n    The name is ending with the name of the previous field.",
        ),
    ]
    assert doc_strings == expected_doc_strings
