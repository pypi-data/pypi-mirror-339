"""Declaration of all config settings."""

import inspect
import re
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from enum import Enum

from hvlbuzz.physics.sound import Season, Weather


class OffsetUnit(Enum):
    """Acoustic Power Unit."""

    pw_m = 120.0
    """dB over 1 pW/m"""
    w_m = 0.0
    """dB over 1 W/m"""


@dataclass
class ConductorScatterPlot:
    """Conductor Scatter Plot."""

    radius_mult: float = 15.0
    """Radius Multiplier

    Multiply the bundle separation radius for graphical presentation only."""
    auto_axis: bool = False
    """Automatic Y-Axis Limits

    If switched on, the limits of the axis will be defined automatically and the values
    below are ignored."""
    lower_axis: float = 20.0
    """Lower Y-Axis Limit [m]

    Manually define the lower axis limit."""

    upper_axis: float = 80.0
    """Upper Y-Axis Limit [m]

    Manually define the upper axis limit."""


class Color(Enum):
    """Available colors to choose in dialogs."""

    red = "red"
    blue = "blue"
    green = "green"
    cyan = "cyan"
    magenta = "magenta"
    yellow = "yellow"
    black = "black"


@dataclass
class ColorConfig:
    """Color."""

    ac_con_color: Color = Color.blue
    """AC Conductor Color

    Choose the color for the line midpoint scatter."""

    dc_pos_con_color: Color = Color.red
    """DC Positive Conductor Color

    Choose the color for the line midpoint scatter."""

    dc_neg_con_color: Color = Color.green
    """DC Negative Conductor Color

    Choose the color for the line midpoint scatter."""

    dc_neut_con_color: Color = Color.black
    """DC Neutral Conductor Color

    Choose the color for the line midpoint scatter."""

    gnd_con_color: Color = Color.black
    """Ground Conductor Color

    Choose the color for the line midpoint scatter."""


@dataclass
class TowerGeometryConfig:
    """Tower Geometry."""

    scatter_plot: ConductorScatterPlot
    color: ColorConfig


@dataclass
class ElectricFieldGeneralConfig:
    """General Config."""

    num_contour: int = 60
    """Number of Contour Points

    Increasing the number of contour points will increase the accuracy of the electric
    field computation but also the calculation time. The input should be an integer
    with a minimum value of 2.
    """


@dataclass
class ElectricFieldGroundPoints:
    """Ground Points."""

    height_above_ground: float = 1.5
    """Height Above Ground [m]

    Define the height above ground where the electric field should be calculated. Since the
    horizontal component of the electric field is ignored, the calculation is more accurate
    for lower heights above ground.
    """
    ground_points_start: float = -60.0
    """Horizontal Ground Points Start [m]

    Define the starting value of the ground points range."""
    ground_points_end: float = 60.0
    """Horizontal Ground Points End [m]

    Define the last value of the ground points range."""
    ground_points_n: int = 121
    """Number of Ground Points

    Number of points within the range where the field will be computed."""


@dataclass
class YAxis:
    """Y-Axis configuration."""

    auto_axis: bool = False
    lower_axis: float = 0.0
    upper_axis: float = 20.0


@dataclass
class ElectricFieldYAxis(YAxis):
    """Y-Axis."""

    auto_axis: bool = False
    """Automatic Y-Axis Limits

    If switched on, the limits of the axis will be defined automatically and the values
    below are ignored."""
    lower_axis: float = 0.0
    """Lower Y-Axis Limit [kV/cm]

    Manually define the lower axis limit."""
    upper_axis: float = 20.0
    """Upper Y-Axis Limit [kV/cm]

    Manually define the upper axis limit."""


@dataclass
class ElectricFieldConfig:
    """Electric Field."""

    general_config: ElectricFieldGeneralConfig
    ground_points: ElectricFieldGroundPoints
    y_axis: ElectricFieldYAxis


@dataclass
class MagneticFieldGroundPoints:
    """Ground Points."""

    height_above_ground: float = 1.5
    """Height Above Ground [m]

    Define the height above ground where the magnetic field should be calculated."""
    ground_points_start: float = -60.0
    """Horizontal Ground Points Start [m]

    Choose the starting value of the ground points range."""
    ground_points_end: float = 60.0
    """Horizontal Ground Points End [m]

    Choose the last value of the ground points range."""
    ground_points_n: int = 121
    """Number of Ground Points

    Number of points within the range where the magnetic field will be computed."""


@dataclass
class MagneticFieldYAxis(YAxis):
    """Y-Axis."""

    auto_axis: bool = False
    """Automatic Y-Axis Limits

    If switched on, the limits of the axis will be defined automatically and the values
    below are ignored."""
    lower_axis: float = 0.0
    """Lower Y-Axis Limit [µT]

    Manually define the lower axis limit."""
    upper_axis: float = 100.0
    """Upper Y-Axis Limit [µT]

    Manually define the upper axis limit."""


@dataclass
class MagneticFieldConfig:
    """Magnetic Field."""

    ground_points: MagneticFieldGroundPoints
    y_axis: MagneticFieldYAxis


@dataclass
class SoundGroundPoints:
    """Ground Points."""

    height_above_ground: float = 1.5
    """Height Above Ground [m]

    Define the height above ground where the sound pressure/power levels should be calculated."""
    ground_points_start: float = -60.0
    """Horizontal Ground Points Start [m]

    Choose the starting value of the ground points range."""

    ground_points_end: float = 60.0
    """Horizontal Ground Points End [m]

    Choose the last value of the ground points range."""

    ground_points_n: int = 121
    """Number of Ground Points

    Number of points within the range where the audible noise will be computed."""


@dataclass
class SoundYAxis(YAxis):
    """Y-Axis."""

    auto_axis: bool = True
    """Automatic Y-Axis Limits

    If switched on, the limits of the axis will be defined automatically and the values below
    are ignored."""

    lower_axis: float = 20.0
    """Lower Y-Axis Limit [dB]

    Manually define the lower axis limit."""

    upper_axis: float = 80.0
    """Upper Y-Axis Limit [dB]

    Manually define the upper axis limit."""


@dataclass
class SoundGeneralSettings:
    """General Calculation Settings."""

    an_unit: OffsetUnit = OffsetUnit.pw_m
    """Acoustic Power Unit

    Choose the unit for the acoustic power calculation."""

    altitude: float = 300.0
    """Altitude Correction

    The altitude above sea level [m]."""

    ac_rain_intensity: float = 0.8
    """Rain Correction

    The correction of the entered rain rate is applied to all AC audible noise computations in
    foul weather according to the EPRI Transmission Line Ref Book ed. 3, unless the old constant
    rain rate correction according to EMPA report 453574-2 is selected (see below).
    Valid values are between 0.1-30 mm/h, otherwise the default 0.8 mm/h is used."""


@dataclass
class AcEpri:
    """AC EPRI."""

    enabled: bool = True
    """Calculate AC EPRI

    Include the AC audible noise calculation according to EPRI if switched on."""

    weather: Weather = Weather.Foul
    """Weather

    Choose the weather condition for the AC EPRI audible noise calculation."""

    offset: bool = False
    """Offset

    Return the audible noise values including DC offset switched on."""

    use_efield_independent_rain_correction: bool = False
    """Use previous field strength independent rain rate correction

    When this switch is set to "on", the former rain rate correction used in the HVLBUZZ program
    until 2023 is applied (only in the EPRI and BPA method). This correction following EMPA
    report no. 452'574-2, version 2016 is no longer recommended (see explanation in the HVLBUZZ
    description document): This method ads a rain rate correction value to the previously
    calculated noise level for "wet conductors" (rain rate 0.75mm/h). This correction neglects
    the dependence on the conductor-surface field strength and is only valid for specific field
    strength values that are above the usual values. The correction curve can be found in Figure
    6.4.35, EPRI Transmission Line Reference Book 345 kV and above, ed. 2, 1982. For this reason,
    the updated field strength dependent correction according to the "EPRI Transmission Line
    Reference Book 345 kV and Above, ed. 3, 2006" is recommended (switch set to "off").
    """


@dataclass
class AcBpa:
    """AC BPA."""

    enabled: bool = True
    """Calulate AC BPA

    Include the AC audible noise calculation according to BPA if switched on."""

    weather: Weather = Weather.Foul
    """Weather

    Choose the weather condition for the AC BPA audible noise calculation."""

    offset: bool = False
    """Offset

    Return the audible noise values including DC offset switched on."""

    use_efield_independent_rain_correction: bool = False
    """Use previous field strength independent rain rate correction

    When this switch is set to "on", the former rain rate correction used in the HVLBUZZ program
    until 2023 is applied (only in the EPRI and BPA method). This correction following EMPA
    report no. 452'574-2, version 2016 is no longer recommended (see explanation in the HVLBUZZ
    description document): This method ads a rain rate correction value to the previously
    calculated noise level for "wet conductors" (rain rate 0.75mm/h). This correction neglects
    the dependence on the conductor-surface field strength and is only valid for specific field
    strength values that are above the usual values. The correction curve can be found in Figure
    6.4.35, EPRI Transmission Line Reference Book 345 kV and above, ed. 2, 1982. For this reason,
    the updated field strength dependent correction according to the "EPRI Transmission Line
    Reference Book 345 kV and Above, ed. 3, 2006" is recommended (switch set to "off").
    """


@dataclass
class AcBpaMod:
    """AC BPA MOD."""

    enabled: bool = True
    """Calulate AC BPA MOD

    Include the AC audible noise calculation according to BPA MOD if switched on."""

    weather: Weather = Weather.Foul
    """Weather

    Choose the weather condition for the AC BPA audible noise calculation."""

    offset: bool = False
    """Offset

    Return the audible noise values including DC offset switched on."""


@dataclass
class AcEdf:
    """AC EDF."""

    enabled: bool = True
    """Calulate AC EDF

    Include the AC audible noise calculation according to EDF if switched on."""

    offset: bool = False
    """Offset

    Return the audible noise values including DC offset switched on."""


@dataclass
class DcEpri:
    """DC EPRI."""

    enabled: bool = True
    """Calculate DC EPRI

    Include the DC audible noise calculation according to EPRI if switched on."""

    weather: Weather = Weather.Fair
    """Weather

    Choose the weather condition for the DC EPRI audible noise calculation."""

    season: Season = Season.Summer
    """Season

    Choose the season for the DC EPRI audible noise calculation."""


@dataclass
class DcBpa:
    """DC BPA."""

    enabled: bool = True
    """Calculate DC BPA

    Include the DC audible noise calculation according to BPA is switched on."""

    weather: Weather = Weather.Fair
    """Weather

    Choose the weather condition for the DC BPA audible noise calculation."""

    season: Season = Season.Summer
    """Season

    Choose the season for the DC BPA audible noise calculation."""


@dataclass
class DcCriepi:
    """DC CRIEPI."""

    enabled: bool = True
    """DC CRIEPI

    Include the DC audible noise calculation according to CRIEPI if switched on."""


@dataclass
class SoundConfig:
    """Audible Noise."""

    ground_points: SoundGroundPoints
    y_axis: SoundYAxis
    general_settings: SoundGeneralSettings
    ac_epri: AcEpri
    ac_bpa: AcBpa
    ac_bpa_mod: AcBpaMod
    ac_edf: AcEdf
    dc_epri: DcEpri
    dc_bpa: DcBpa
    dc_criepi: DcCriepi


class CsvSeparator(Enum):
    """Available values for delimiters used for csv export."""

    semicolon = ";"
    comma = ","


class DecimalSeparator(Enum):
    """Available values for decimal separator used for csv export."""

    point = "."
    comma = ","


@dataclass
class ExportConfig:
    """Export."""

    csv_delimiter: CsvSeparator = CsvSeparator.semicolon
    """Column Separator

    Choose the delimiter between entries in the CSV file."""

    csv_decimal: DecimalSeparator = DecimalSeparator.point
    """Decimal Separator

    Choose the decimal separator for number entries in the CSV file."""

    load_path: str = "default load path"
    """Load path"""
    save_path: str = "default save path"
    """Save path"""
    csv_path: str = "default csv path"
    """csv path"""
    pdf_path: str = "default pdf path"
    """pdf path"""
    png_path: str = "default png path"
    """png path"""


@dataclass
class Config:
    """Top level config."""

    tower_geometry: TowerGeometryConfig
    electric_field: ElectricFieldConfig
    magnetic_field: MagneticFieldConfig
    sound: SoundConfig
    export: ExportConfig


def extract_attribute_doc_strings(
    c: type, field_names: Callable[[type], list[str]]
) -> Iterable[tuple[str, str]]:
    """Parse the code of a dataclass or enum to collect attribute docstrings.

    Have to do that manually as such docstrings are not available during runtime.
    """
    code = inspect.getsource(c)
    for f in field_names(c):
        m = re.compile(rf'^ *{f}(:| ?=).*\n *"""(?P<doc>(.|\n)+?)"""', flags=re.MULTILINE).search(
            code
        )
        if m is None:
            continue
        yield f, m["doc"]
