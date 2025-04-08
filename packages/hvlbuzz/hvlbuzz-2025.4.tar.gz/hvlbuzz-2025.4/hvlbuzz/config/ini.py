"""Load config from buzz.ini."""

import os
from collections.abc import Iterable
from dataclasses import fields, is_dataclass
from enum import Enum
from typing import Any, TypeVar, cast

from kivy.config import ConfigParser

from hvlbuzz.config.config import Config, extract_attribute_doc_strings
from hvlbuzz.config.field_names import enum_field_names


class ConfigLoader:
    """Config manager."""

    def __init__(self) -> None:
        self.data = load_ini()

    def update(self) -> None:
        """Reload config."""
        self.data = load_ini()


def buzz_ini_path() -> str:
    """Path were to persist dialog settings for the GUI."""
    ini_folder = os.path.join(
        (os.getenv("APPDATA") or "") if os.name == "nt" else os.path.expanduser("~/.config"),
        "hvlbuzz",
    )

    os.makedirs(ini_folder, exist_ok=True)
    return os.path.join(ini_folder, "buzz.ini")


def load_ini(path: str = buzz_ini_path()) -> Config:
    """Load full config from an ini file."""
    parser = ConfigParser()
    parser.read(path)
    return load_ini_section_from_parser(parser, Config)


def format_ini_section(section_path: tuple[str, ...]) -> str:
    """Format a hierarchy of sections to a ini section name."""
    # Omit root section:
    return "|".join(section_path[1:])


T = TypeVar("T")


def load_ini_section_from_parser(
    parser: ConfigParser, c: type[T], parent_sections: tuple[str, ...] = ()
) -> T:
    """Instantiate T initializing fields with values loaded from an ini parser."""
    section_path = (*parent_sections, config_section_name(c))
    assert is_dataclass(c)
    arguments_raw = (
        (f.name, f.type, parser.get(format_ini_section(section_path), f.name, fallback=None))
        for f in fields(c)
        if not is_dataclass(f.type) and isinstance(f.type, type)
    )
    arguments: dict[str, Any] = {
        key: deserialize(t, val) for (key, t, val) in arguments_raw if val is not None
    }
    sub_sections: dict[str, Any] = {
        f.name: load_ini_section_from_parser(parser, f.type, parent_sections=section_path)
        for f in fields(c)
        if is_dataclass(f.type) and isinstance(f.type, type)
    }
    return cast("T", c(**arguments, **sub_sections))


def config_section_name(c: type) -> str:
    """Create a section name for a data class based on its doc string."""
    if c.__doc__ is None:
        return ""
    return c.__doc__.splitlines()[0]


E = TypeVar("E", bound=Enum)


def deserialize(t: type[T], value: str) -> T:
    """Deserialize a primitive value."""
    if issubclass(t, Enum):
        return cast("T", deserialize_enum(t, value))
    if t is bool:
        return cast("T", bool(int(value)))
    return t(value)  # type: ignore[call-arg]


def deserialize_enum(t: type[E], value: str) -> E:
    """Deserialize an enum from a str.

    If the enum is not string valued, use its doc strings to deserialize.
    """
    try:
        return t(value)
    except ValueError:
        variant_mapping = {doc: variant for variant, doc in enum_variants(t)}
        return variant_mapping[value]


def serialize_enum(value: Enum) -> str:
    """Serialize an enum to a str.

    If the enum is not string valued, use its doc strings to serialize.
    """
    s = value.value
    if isinstance(s, str):
        return s
    variant_mapping = dict(enum_variants(type(value)))
    return variant_mapping[value]


def enum_variants(t: type[E]) -> Iterable[tuple[E, str]]:
    """Extract the doc strings from a type and generate (variant, doc) tuples."""
    return (
        (variant, doc)
        for (_, doc), variant in zip(extract_attribute_doc_strings(t, enum_field_names), t)
    )
