"""Build settings panels based on a dataclass."""

from __future__ import annotations

from dataclasses import MISSING, fields, is_dataclass
from enum import Enum
from typing import TYPE_CHECKING, Any

from kivy.uix.settings import (
    SettingBoolean,
    SettingNumeric,
    SettingOptions,
    SettingsPanel,
    SettingString,
    SettingTitle,
)

from hvlbuzz.config.config import extract_attribute_doc_strings
from hvlbuzz.config.field_names import dataclass_field_names, enum_field_names
from hvlbuzz.config.ini import config_section_name, format_ini_section, serialize_enum

if TYPE_CHECKING:
    from collections.abc import Iterable

    import kivy


def set_defaults(config_type: type, config: kivy.config.Config) -> None:
    """Define the default values for config."""
    for section_path, defaults in extract_defaults(config_type):
        config.setdefaults(
            format_ini_section(section_path),
            {key: serialize_ini_value(val) for key, val in defaults.items()},
        )


def serialize_ini_value(val: Any) -> Any:
    """Serialize a config value to a representation, kivy can correctly parse."""
    if isinstance(val, Enum):
        return serialize_enum(val)
    if isinstance(val, bool):
        return int(val)
    return val


def extract_defaults(
    c: type, parent_sections: tuple[str, ...] = ()
) -> Iterable[tuple[tuple[str, ...], dict[str, Any]]]:
    """Recursively extract all default values from a dataclass."""
    assert is_dataclass(c)
    assert c.__doc__ is not None
    section_path = (*parent_sections, config_section_name(c))
    defaults = {
        field.name: field.default
        for field in fields(c)
        if not is_dataclass(field.type) and field.default is not MISSING
    }
    if defaults:
        yield (section_path, defaults)
    for field in fields(c):
        if is_dataclass(field.type) and isinstance(field.type, type):
            yield from extract_defaults(field.type, parent_sections=section_path)


def settings_add_dataclass_panels(
    settings: kivy.uix.settings.Settings, c: type, config: kivy.config.Config
) -> None:
    """Add SettingsPanel instances based on a dataclass to a settings instance using config.

    The dataclass servces as a top level config structure. All its direct
    dataclass attributes will yield an own panel.
    """
    title = c.__doc__ or ""
    for f in fields(c):
        if is_dataclass(f.type) and isinstance(f.type, type):
            settings_add_dataclass_panel(settings, f.type, config, title)


def settings_add_dataclass_panel(
    settings: kivy.uix.settings.Settings,
    c: type,
    config: kivy.config.Config,
    parent_section: str,
    title: str | None = None,
) -> None:
    """Add a SettingsPanel based on a dataclass to a settings instance using config."""
    assert is_dataclass(c)
    if title is None:
        title = c.__doc__ or ""
    panel = SettingsPanel(title=title, settings=settings, config=config)
    for widget in panel_widgets_from_dataclass(
        c,
        panel,
        parent_sections=(parent_section,),
    ):
        panel.add_widget(widget)
    uid = panel.uid
    if settings.interface is not None:
        settings.interface.add_panel(panel, title, uid)


def panel_widgets_from_dataclass(
    c: type,
    panel: SettingsPanel,
    parent_sections: tuple[str, ...] = (),
) -> Iterable[kivy.uix.widget.Widget]:
    """Build a settings panel based on a dataclass."""
    assert is_dataclass(c)
    assert c.__doc__ is not None
    section_path = (*parent_sections, config_section_name(c))
    attribute_docs = dict(extract_attribute_doc_strings(c, dataclass_field_names))
    for field in fields(c):
        if is_dataclass(field.type) and isinstance(field.type, type):
            yield SettingTitle(text=field.type.__doc__)
            yield from panel_widgets_from_dataclass(field.type, panel, parent_sections=section_path)
            continue
        title, desc = split_docstr(attribute_docs.get(field.name, "\n"))
        arguments = {
            "title": title,
            "desc": desc,
            "key": field.name,
            "section": format_ini_section(section_path),
            "panel": panel,
        }
        if field.type is bool:
            yield SettingBoolean(**arguments)
        elif field.type in (float, int):
            yield SettingNumeric(**arguments)
        elif field.type is str:
            yield SettingString(**arguments)
        elif isinstance(field.type, type) and issubclass(field.type, Enum):
            variants = [v.value for v in field.type]
            if not all(isinstance(v, str) for v in variants):
                variants = [
                    doc for _, doc in extract_attribute_doc_strings(field.type, enum_field_names)
                ]
            yield SettingOptions(options=variants, **arguments)


def split_docstr(text: str) -> tuple[str, str]:
    """Split an attribute docstring into title and description."""
    try:
        title, desc = text.split("\n", 1)
    except ValueError:
        title = text
        desc = ""
    desc = desc.replace("\n\n", "\0").replace("\n", "").replace("\0", "\n").replace("    ", " ")
    return title.strip(), desc.strip()
