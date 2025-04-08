"""Shared functionality for output (csv / pdf)."""

from datetime import datetime

from hvlbuzz.config.config import Config
from hvlbuzz.config.ini import serialize_enum


def settings_data_rows(config_path: str, cfg: Config) -> list[list[str]]:
    """Assembles info about settings in table format (nested list of strings)."""
    return [
        ["Loaded JSON File:", config_path],
        [
            "Report Generated on:",
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        ],
        ["Number of Contour Points (CSM):", str(cfg.electric_field.general_config.num_contour)],
        ["Altitude:", str(cfg.sound.general_settings.altitude)],
        [
            "Rain Rate (default is 0.8):",
            str(cfg.sound.general_settings.ac_rain_intensity),
        ],
        ["AC EPRI Weather:", serialize_enum(cfg.sound.ac_epri.weather)],
        [
            "AC EPRI DC Offset:",
            str(bool(cfg.sound.ac_epri.offset)),
        ],
        ["AC BPA Weather:", serialize_enum(cfg.sound.ac_bpa.weather)],
        ["AC BPA DC Offset:", str(cfg.sound.ac_bpa.offset)],
        ["DC EPRI Weather:", serialize_enum(cfg.sound.dc_epri.weather)],
        ["DC EPRI Season:", serialize_enum(cfg.sound.dc_epri.season)],
        ["DC BPA Weather:", serialize_enum(cfg.sound.dc_bpa.weather)],
        ["DC BPA Season:", serialize_enum(cfg.sound.dc_bpa.season)],
    ]
