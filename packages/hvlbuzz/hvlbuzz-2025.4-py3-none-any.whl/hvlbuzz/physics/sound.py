"""Sound routines."""

from collections.abc import Callable, Iterable
from dataclasses import dataclass
from enum import Enum
from typing import ClassVar, TypeVar

import numpy as np
from numpy.typing import NDArray

from .line import Line, LineType
from .system import System, SystemType


class Season(Enum):
    """Seasons for audible noise correction."""

    Summer = "summer"
    Winter = "winter"
    Fall = "fall"
    Spring = "spring"


class Weather(Enum):
    """Weather condition."""

    Fair = "fair"
    Foul = "foul"


@dataclass
class AcSoundRoutineParameters:
    """Abstract collection of parameters for a AC sound routine."""

    name: ClassVar[str]
    reference_rate: ClassVar[float]
    """Rain rate [mm/h] corresponding to the correction term delta_A."""

    def calc(self, line: Line, ground_points: NDArray[np.float64], E: float) -> tuple[float, float]:
        """Compute the sound pressure level for a line.

        :param line: Line to compute values for.
        :param ground_points: Numpy array containing x and y coordinates of ground points
           (shape (2, n)).
        :param E: Relevant E field value from a Line instance (e.g. E_ac, E_ac_pos_offset).

        :return: Tuple consisting of the P_50 value and the A_50 value.
        """
        msg = "Must be implemented"
        raise NotImplementedError(msg)

    def calc_systems(
        self,
        systems: list[System],
        ground_points: NDArray[np.float64],
    ) -> tuple[NDArray[np.float64], list[tuple[Line, float]]]:
        """Combine values of single lines to a total value for each given ground point.

        :param systems: Systems to compute values for.
        :param ground_points: Numpy array containing x and y coordinates of ground points
          (shape (2, n)).

        :return: tuple consisting of:

        - Numpy array containing the sound pressure levels without DC bias.
          The sound pressure level is calculated for each ground point used as input.
        - Values per line as a list of (line, A value) tuples.

        """
        lines = collect_ac_lines(systems)
        P_50, A_50 = unzip_2(self.calc(line, ground_points, line.E_ac) for line in lines)

        return p_50_sum(np.array(P_50)), list(zip(lines, A_50))

    def calc_systems_offset(
        self,
        systems: list[System],
        ground_points: NDArray[np.float64],
    ) -> tuple[NDArray[np.float64], list[tuple[Line, float]]]:
        """Same as `calc_systems` but with offset values."""
        lines = collect_ac_lines(systems)
        P_50, A_50 = unzip_2(self.calc(line, ground_points, line.E_ac_pos_offset) for line in lines)

        return p_50_sum(np.array(P_50)), list(zip(lines, A_50))

    @classmethod
    def rain_correction(cls, rain_rate: float, E: float, line: Line) -> float:
        """Same as `delta_rain` with `reference_rate=cls.reference_rate`."""
        return delta_rain(rain_rate, E, line, cls.reference_rate)


def collect_ac_lines(systems: list[System]) -> list[Line]:
    """Collect AC lines of all systems."""
    return [
        line for system in systems if system.system_type == SystemType.ac for line in system.lines
    ]


@dataclass
class AcSoundRoutineParametersWorstCaseOffset(AcSoundRoutineParameters):
    """Abstract collection of parameters for a AC sound routine.

    Using worse of the positive and negative DC bias are chosen as the offset.
    """

    name: ClassVar[str]

    def calc(self, line: Line, ground_points: NDArray[np.float64], E: float) -> tuple[float, float]:
        """Compute the sound pressure level for a line.

        :param line: Line to compute values for.
        :param ground_points: Numpy array containing x and y coordinates of ground points
          (shape (2, n)).
        :param E: Relevant E field value from a Line instance (e.g. E_ac, E_ac_pos_offset).

        :return: Tuple consisting of the P_50 value and the A_50 value.
        """
        msg = "Must be implemented"
        raise NotImplementedError(msg)

    def calc_systems_offset(
        self,
        systems: list[System],
        ground_points: NDArray[np.float64],
    ) -> tuple[NDArray[np.float64], list[tuple[Line, float]]]:
        """Same as `calc_systems` but with offset values.

        The worse of the positive and negative DC bias are chosen as the offset.
        Used by the EPRI method.
        """
        lines = collect_ac_lines(systems)

        P_50_pos_offset = []
        P_50_neg_offset = []
        A_50 = []

        for line in lines:
            P_50_p, A_50_pos_offset = self.calc(
                line,
                ground_points,
                line.E_ac_pos_offset,
            )
            P_50_n, A_50_neg_offset = self.calc(
                line,
                ground_points,
                line.E_ac_neg_offset,
            )
            if line.num_con < 3:
                # calculate acoustic power with negative DC offset
                # negative Trichel pulses emits lower noise level
                # thus, 4dB is subtracted from negative offset
                A_50_neg_offset -= 4.0
                P_50_n -= 4.0
            A_50.append((line, np.maximum(A_50_pos_offset, A_50_neg_offset)))
            P_50_pos_offset.append(P_50_p)
            P_50_neg_offset.append(P_50_n)
        P_50_sum_pos_offset = p_50_sum(np.array(P_50_pos_offset))
        P_50_sum_neg_offset = p_50_sum(np.array(P_50_neg_offset))
        if np.max(P_50_sum_pos_offset) > np.max(P_50_sum_neg_offset):
            return P_50_sum_pos_offset, A_50
        return P_50_sum_neg_offset, A_50


@dataclass
class DcSoundRoutineParametersBase:
    """Base class for `DcSoundRoutineParameters` and `DcCriepi`."""

    name: ClassVar[str]

    def calc_systems(
        self,
        systems: list[System],
        ground_points: NDArray[np.float64],
    ) -> tuple[NDArray[np.float64], list[tuple[Line, float]]]:
        """Combine values of single lines to a total value for each given ground point.

        :param systems: Systems to compute values for.
        :param ground_points: Numpy array containing x and y coordinates of ground points
          (shape (2, n)).

        :return: tuple consisting of:

        - Numpy array containing the sound pressure levels without DC bias.
          The sound pressure level is calculated for each ground point used as input.
        - Values per line as a list of (line, A value) tuples.

        """
        msg = "Must be implemented"
        raise NotImplementedError(msg)


@dataclass
class DcSoundRoutineParameters(DcSoundRoutineParametersBase):
    """Abstract collection of parameters for a DC sound routine."""

    def calc(self, line: Line, ground_points: NDArray[np.float64]) -> tuple[float, float]:
        """Compute the sound pressure level.

        :param line: Line to compute values for.
        :param ground_points: Numpy array containing x and y coordinates of ground points
          (shape (2, n)).

        :return: Tuple consisting of the P_50 value and the A_50 value.
        """
        msg = "Must be implemented"
        raise NotImplementedError(msg)

    def calc_systems(
        self,
        systems: list[System],
        ground_points: NDArray[np.float64],
    ) -> tuple[NDArray[np.float64], list[tuple[Line, float]]]:
        """Combine values of single lines to a total value for each given ground point.

        :param systems: Systems to compute values for.
        :param ground_points: Numpy array containing x and y coordinates of ground points
          (shape (2, n)).

        :return: tuple consisting of:

        - Numpy array containing the sound pressure levels without DC bias.
          The sound pressure level is calculated for each ground point used as input.
        - Values per line as a list of (line, A value) tuples.

        """
        lines = collect_dc_lines(systems)
        P_50, A_50 = unzip_2(self.calc(line, ground_points) for line in lines)

        return p_50_sum(np.array(P_50)), list(zip(lines, A_50))


A = TypeVar("A")
B = TypeVar("B")


def unzip_2(zipped: Iterable[tuple[A, B]]) -> tuple[tuple[A, ...], tuple[B, ...]]:
    """Variant of `zip(*iterable)` which supports empty iterables."""
    try:
        a, b = zip(*zipped)
    except ValueError:
        return (), ()
    return a, b


def collect_dc_lines(systems: list[System]) -> list[Line]:
    """Collect DC lines of all systems."""
    return [
        line
        for system in systems
        if system.system_type in {SystemType.dc, SystemType.dc_bipol}
        for line in system.lines
        if line.line_type != LineType.dc_neut
    ]


def compute_E_c(n: int, d: float) -> float:
    """6-dB gradient."""
    E_c: float = 24.4 / d**0.24
    if n > 8:
        E_c -= (n - 8) / 4
    return E_c


def compute_delta_A_from_E_c(n: int, d: float, d_bundle: float, E: float, E_c: float) -> float:
    """EPRI correction heavy rain (6.5mm/h) -> wet conductor (0.75mm/h).

    Routine using precomputed E_c.
    """
    delta = -14.2 * E_c / E
    if n < 3:
        return 8.2 + delta
    return 10.4 + delta + 8 * (n - 1) * d / d_bundle


def compute_delta_A(n: int, d: float, d_bundle: float, E: float) -> float:
    """EPRI correction heavy rain (6.5mm/h) -> wet conductor (0.75mm/h)."""
    return compute_delta_A_from_E_c(n, d, d_bundle, E, compute_E_c(n, d))


def delta_rain(rain_rate: float, E: float, line: Line, reference_rate: float) -> float:
    """Field strength weighted rain rate correction relative to a reference rain rate.

    Reference rate: `r_wc = 0.75mm/h` according to EPRI.

    :param rain_rate: Rain rate for which to compute the correction.
    :param E: Electric field strength.
    :param line: Properties of the line.
    :param reference_rate: Rain rate [mm/h] corresponding to the correction term delta_A.
    """
    r_hr = 6.5  # Heavy rain rate [mm/h]
    r_wc = 0.75  # Light rain (wet conductors) rate [mm/h]
    d = line.con_radius * 2 * 100.0  # radius [m] -> diameter [cm]
    d_bundle = line.bundle_radius * 2 * 100.0  # radius [m] -> diameter [cm]
    delta_A = compute_delta_A(line.num_con, d, d_bundle, E)
    correction: float = -delta_A * np.log10(rain_rate / reference_rate) / np.log10(r_hr / r_wc)
    return correction


@dataclass
class AcEpri(AcSoundRoutineParametersWorstCaseOffset):
    """Empirical formula defined by EPRI for AC lines."""

    name: ClassVar[str] = "AC EPRI"
    reference_rate: ClassVar[float] = 6.5

    weather: Weather
    """weather conditions. One of:
        * Foul: default weather condition for the AC EPRI calculation
        * Fair: reduces the audible noise by 25dB
    """
    altitude: float
    """audible noise altitude correction [m]"""
    rain_rate: float
    """Rain rate for the inclusion of rain factor correction in calculation"""
    use_efield_independent_rain_correction: bool = False
    """Look up the correction in a table (field strength independent)
    instead of using a field strength weighted rain rate correction.
    """

    def __post_init__(self) -> None:
        """E field independent rain correction is made available here.

        For backwards compatibility.
        """
        self._rain_correction: Callable[[Weather, float, float, Line], float]
        if self.use_efield_independent_rain_correction:
            self._rain_correction = delta_rain_table_lookup_plus_delta_A
        else:
            self._rain_correction = lambda _weather, *args: self.rain_correction(*args)

    def calc(self, line: Line, ground_points: NDArray[np.float64], E: float) -> tuple[float, float]:
        """Compute the sound pressure level.

        :param line: Line to compute values for.
        :param ground_points: Numpy array containing x and y coordinates of ground points
          (shape (2, n)).
        :param E: Relevant E field value from a Line instance (e.g. E_ac, E_ac_pos_offset).

        :return: Tuple consisting of the P_50 value and the A_50 value.
        """

        # rename the number of suubconductor variable for convenience
        n_sc = line.num_con
        # conversion from radius [m] to diameter [cm]
        sc_d = line.con_radius * 2 * 100
        bun_d = line.bundle_radius * 2 * 100

        E_ac = E
        # calculate the heavy rain acoustic power in dBA above 1W/m
        if n_sc < 3:
            # define calculation constants
            k = 7.5 if n_sc == 1 else 2.6

            A_5 = 20.0 * np.log10(n_sc) + 44.0 * np.log10(sc_d) - 665.0 / E_ac + k - 39.1
        else:
            A_5 = (
                20.0 * np.log10(n_sc)
                + 44.0 * np.log10(sc_d)
                - 665.0 / E_ac
                + 22.9 * (n_sc - 1) * sc_d / bun_d
                - 46.4
            )

        # Measurable rain acoustic power in dB:
        A_50 = (
            A_5
            + self._rain_correction(self.weather, self.rain_rate, E_ac, line)
            + altitude_correction(self.altitude)
        )

        # Distance between the line and ground points:
        dist = np.hypot(ground_points[0] - line.line_x, ground_points[1] - line.line_y)

        # subtract 25 dB for fair weather
        if self.weather == Weather.Fair:
            A_50 -= 25.0

        # Sound pressure levels in dBA:
        P_50 = A_50 + 114.3 - (10.0 * np.log10(dist) + 0.02 * dist)

        return P_50, A_50


@dataclass
class AcBpa(AcSoundRoutineParameters):
    """Empirical formula defined by BPA for AC lines."""

    name: ClassVar[str] = "AC BPA"
    reference_rate: ClassVar[float] = 1.0

    weather: Weather
    """weather conditions. One of:
        * Fair: default weather condition for the DC BPA calculation
        * Foul: reduces the audible noise by 6dB
    """
    altitude: float
    """audible noise altitude correction [m]"""
    rain_rate: float
    """Rain rate for the inclusion of rain factor correction in calculation"""
    use_efield_independent_rain_correction: bool = False
    """Look up the correction in a table (field strength independent)
    instead of using a field strength weighted rain rate correction.
    """

    def __post_init__(self) -> None:
        """The E field independent rain correction is made available here.

        For backwards compatibility.
        """
        self._rain_correction: Callable[[Weather, float, float, Line], float]
        if self.use_efield_independent_rain_correction:
            self._rain_correction = delta_rain_table_lookup
        else:
            self._rain_correction = lambda _weather, *args: self.rain_correction(*args)

    def calc(self, line: Line, ground_points: NDArray[np.float64], E: float) -> tuple[float, float]:
        """Compute the sound pressure level.

        :param line: Line to compute values for.
        :param ground_points: Numpy array containing x and y coordinates of ground points
          (shape (2, n)).
        :param E: Relevant E field value from a Line instance (e.g. E_ac, E_ac_pos_offset).

        :return: Tuple consisting of the P_50 value and the A_50 value.
        """

        # rename the number of subconductor variable for convenience
        n_sc = line.num_con
        # conversion from radius [m] to diameter [cm]
        sc_d = line.con_radius * 2 * 100

        # define calculation constants
        if 0 < n_sc < 3:
            k = 0.0
            AN_0 = -115.4
        else:
            k = 26.4
            AN_0 = -128.4

        # calculate the heavy rain acoustic power in dBA above 1W/m
        L_w50 = (
            120 * np.log10(E)
            + k * np.log10(n_sc)
            + 55 * np.log10(sc_d)
            + AN_0
            - 114.3
            + altitude_correction(self.altitude)
            + self._rain_correction(self.weather, self.rain_rate, E, line)
        )

        # calculate the distance between the line and ground points
        dist = np.hypot(ground_points[0] - line.line_x, ground_points[1] - line.line_y)

        # calculate the sound pressure levels
        L_50 = L_w50 + 114.3 - 11.4 * np.log10(dist)

        # subtract 25 dB for fair weather
        if self.weather == Weather.Fair:
            L_50 -= 25.0
            L_w50 -= 25.0

        return L_50, L_w50


@dataclass
class AcBpaMod(AcSoundRoutineParameters):
    """Empirical formula defined by BPA for AC lines (modified version)."""

    name: ClassVar[str] = "AC BPA MOD"
    reference_rate: ClassVar[float] = 1.0

    weather: Weather
    """weather conditions. One of:
        * Fair: default weather condition for the DC BPA calculation
        * Foul: reduces the audible noise by 6dB
    """

    altitude: float
    """audible noise altitude correction [m]"""
    rain_rate: float
    """Rain rate for the inclusion of rain factor correction in calculation"""

    def calc(self, line: Line, ground_points: NDArray[np.float64], E: float) -> tuple[float, float]:
        """Compute the sound pressure level.

        :param line: Line to compute values for.
        :param ground_points: Numpy array containing x-coordinates of ground points.
        :param E: Relevant E field value from a Line instance (e.g. E_ac, E_ac_pos_offset).

        :return: Tuple consisting of the P_50 value and the A_50 value.
        """

        # rename the number of subconductor variable for convenience
        n = line.num_con
        # conversion from radius [m] to diameter [cm]
        d = line.con_radius * 2.0 * 100.0

        # calculate the 1mm/h rain acoustic power in dBA above 1µW/m
        L_w50 = (
            -127.0
            + 83.0 * np.log10(E - 5.8)
            + 55.0 * np.log10(d)
            + 7.1 * np.log10(n**4.3 + 193.0)
            + altitude_correction(self.altitude)
            + self.rain_correction(self.rain_rate, E, line)
        )

        # calculate the distance between the line and ground points
        dist = np.hypot(ground_points[0] - line.line_x, ground_points[1] - line.line_y)

        # calculate the sound pressure levels
        L_50 = L_w50 - 10.0 * np.log10(dist) - 0.02 * dist
        L_P0 = L_50 + 54.3

        uW_to_W = -60.0  # conversion from dBA above 1µW/m to dBA above 1W/m
        return L_P0, L_w50 + uW_to_W


@dataclass
class AcEdf(AcSoundRoutineParameters):
    """Empirical formula defined by EDF for AC lines."""

    name: ClassVar[str] = "AC EDF"
    reference_rate: ClassVar[float] = 6.0

    altitude: float
    """Altitude [m]"""
    rain_rate: float
    """Rain rate for the inclusion of rain factor correction in calculation"""

    def calc(self, line: Line, ground_points: NDArray[np.float64], E: float) -> tuple[float, float]:
        """Compute the sound pressure level.

        :param line: Line to compute values for.
        :param ground_points: Numpy array containing x and y coordinates of ground points
          (shape (2, n)).
        :param E: Relevant E field value from a Line instance (e.g. E_ac, E_ac_pos_offset).

        :return: Tuple consisting of the P_50 value and the A_50 value.
        """

        # rename the number of subconductor variable for convenience
        n_sc = line.num_con
        # conversion from radius [m] to diameter [cm]
        sc_d = line.con_radius * 2.0 * 100.0

        L = (
            44.024 * np.log10((E - 6.991) / 0.9883)
            + 4.5 * sc_d
            + 15 * np.log10(n_sc)
            - 114.3
            + altitude_correction(self.altitude)
            + self.rain_correction(self.rain_rate, E, line)
        )

        # calculate the distance between the line and ground points
        dist = np.hypot(ground_points[0] - line.line_x, ground_points[1] - line.line_y)

        # calculate the sound pressure levels
        L_50 = L + 114.3 - (10.0 * np.log10(dist) + 0.02 * dist)

        return L_50, L


@dataclass
class DcEpri(DcSoundRoutineParameters):
    """Empirical formula defined by EPRI for DC lines."""

    name: ClassVar[str] = "DC EPRI"

    weather: Weather
    """weather conditions. One of:
        * Fair: default weather condition for the DC BPA calculation
        * Foul: reduces the audible noise by 6dB
    """
    season: Season
    """One of:
        * Summer: default seasonal condition for the DC EPRI calculation
        * Winter: reduces the audible noise by 4dB
        * Fall/Spring: reduces the audible noise by 2dB
    """
    altitude: float
    """audible noise altitude correction [m]"""

    def calc(self, line: Line, ground_points: NDArray[np.float64]) -> tuple[float, float]:
        """Compute the sound pressure level.

        :param line: Line to compute values for.
        :param ground_points: Numpy array containing x and y coordinates of ground points
          (shape (2, n)).

        :return: Tuple consisting of the P_50 value and the A_50 value.
        """

        # rename the number of suubconductor variable for convenience
        n_sc = line.num_con
        # conversion from radius [m] to diameter [cm]
        sc_d = line.con_radius * 2 * 100

        # define calculation constants
        if n_sc == 1:
            k = 7.5
        elif n_sc == 2:
            k = 2.6
        else:
            k = 0.0

        # calculate the acoustic power
        L_50 = (
            -57.4
            + k
            + 124 * np.log10(np.abs(line.E_dc_rip / 25))
            + 25 * np.log10(sc_d / 4.45)
            + 18 * np.log10(n_sc / 2)
            + altitude_correction(self.altitude)
        )
        if line.E_dc < 0.0:
            L_50 -= 8.0

        # calculate the distance between the line and ground points
        dist = np.hypot(ground_points[0] - line.line_x, ground_points[1] - line.line_y)

        # calculate the sound pressure level in dBA
        P_50 = L_50 + 114.3 - (10.0 * np.log10(dist) + 0.02 * dist)

        # take into account the season
        season_offset = season_dc_offset_epri(self.season)
        P_50 += season_offset

        # subtract 6 dB for foul weather
        if self.weather == Weather.Foul:
            P_50 -= 6.0
            L_50 -= 6.0

        return P_50, L_50 + season_offset


@dataclass
class DcBpa(DcSoundRoutineParameters):
    """Empirical formula defined by BPA for DC lines."""

    name: ClassVar[str] = "DC BPA"

    weather: Weather
    """weather conditions. One of:
        * Fair: default weather condition for the DC BPA calculation
        * Foul: reduces the audible noise by 6dB
    """
    season: Season
    """One of:
        * Fall/Spring: default seasonal condition for the DC BPA calculation
        * Summer: increases the audible noise by 2dB
        * Winter: reduces the audible noise by 2dB
    """
    altitude: float
    """audible noise altitude correction [m]"""

    def calc(self, line: Line, ground_points: NDArray[np.float64]) -> tuple[float, float]:
        """Compute the sound pressure level.

        :param line: Line to compute values for.
        :param ground_points: Numpy array containing x and y coordinates of ground points
          (shape (2, n)).

        :return: Tuple consisting of the P_50 value and the A_50 value.
        """

        # rename the number of suubconductor variable for convenience
        n_sc = line.num_con
        # conversion from radius [m] to diameter [mm]
        sc_d = line.con_radius * 2 * 1000

        # calculate equivalent diameter
        d_eq = sc_d if 0 < n_sc < 3 else sc_d * 0.66 * n_sc**0.64

        # calculate the acoustic power
        L_w50 = (
            -127.6
            + 86 * np.log10(np.abs(line.E_dc_rip))
            + 40 * np.log10(d_eq)
            - 114.3
            + altitude_correction(self.altitude)
        )
        if line.E_dc < 0.0:
            L_w50 -= 8.0

        # calculate the distance between the line and ground points
        dist = np.hypot(ground_points[0] - line.line_x, ground_points[1] - line.line_y)

        L_50 = L_w50 + 114.3 - 5.8 - 11.4 * np.log10(dist)

        # take into account the season

        season_correction = season_dc_offset_bpa(self.season)
        L_50 += season_correction

        # subtract 6 dB for foul weather
        if self.weather == Weather.Foul:
            L_50 -= 6.0
            L_w50 -= 6.0

        return L_50, L_w50 - 5.8 + season_correction


@dataclass
class DcCriepi(DcSoundRoutineParametersBase):
    """Empirical formula defined by CRIEPI for DC lines.

    This class does not inherit from `DcSoundRoutineParameters` as it has
    an additional parameter `dist_bipol` in `calc`.
    """

    name: ClassVar[str] = "DC CRIEPI"

    @staticmethod
    def calc(
        line: Line,
        ground_points: NDArray[np.float64],
        dist_bipol: float,
    ) -> tuple[float, float]:
        """Empirical formula defined by CRIEPI for DC lines.

        :param line: Line to compute values for.
        :param ground_points: Numpy array containing x and y coordinates of ground points
          (shape (2, n)).
        :param dist_bipol: Distance between the positive and the negative conductor
          within the system.

        :return: Tuple consisting of the P_50 value and the A_50 value.
        """
        # rename the number of suubconductor variable for convenience
        n_sc = line.num_con
        # conversion from radius [m] to diameter [cm]
        sc_d = line.con_radius * 2 * 100

        g_50 = 1.0 / (
            np.log10(n_sc) / 91.0 + np.log10(sc_d) / 19.0 + 1.0 / (2 * dist_bipol**2) + 1.0 / 151
        )
        g_60 = 1.0 / (
            np.log10(n_sc) / 71.0 + np.log10(sc_d) / 21.0 + 1.0 / (2.0 * dist_bipol**2) + 1.0 / 1906
        )

        # calculate the acoustic power
        L_w50 = 10.0 * (g_60 / (g_60 - g_50)) * (1.0 - g_50 / np.abs(line.E_dc_rip)) + 50.0 - 114.3
        if line.E_dc < 0.0:
            L_w50 -= 8.0

        # calculate the distance between the line and ground points
        dist = np.hypot(ground_points[0] - line.line_x, ground_points[1] - line.line_y)

        # calculate the sound pressure levels in dBA
        L_50 = L_w50 + 114.3 - 10.0 * np.log10(dist)

        return L_50, L_w50

    def calc_systems(
        self,
        systems: list[System],
        ground_points: NDArray[np.float64],
    ) -> tuple[NDArray[np.float64], list[tuple[Line, float]]]:
        """Combine values of single lines to a total value for each given ground point.

        :param systems: Systems to compute values for.
        :param ground_points: Numpy array containing x and y coordinates of ground points
          (shape (2, n)).

        :return: tuple consisting of:

        - Numpy array containing the sound pressure levels without DC bias.
          The sound pressure level is calculated for each ground point used as input.
        - Values per line as a list of (line, A value) tuples.

        """
        lines = []
        P_50 = []
        A_50 = []

        for system in systems:
            if system.system_type in {SystemType.dc, SystemType.dc_bipol}:
                x_pos, y_pos = np.nan, np.nan
                x_neg, y_neg = np.nan, np.nan
                for line in system.lines:
                    if line.line_type == LineType.dc_neut:
                        continue

                    if line.line_type == LineType.dc_pos:
                        x_pos = line.line_x
                        y_pos = line.line_y
                    elif line.line_type == LineType.dc_neg:
                        x_neg = line.line_x
                        y_neg = line.line_y
                dist_bipol = np.hypot(x_pos - x_neg, y_pos - y_neg)
                for line in system.lines:
                    if line.line_type == LineType.dc_neut:
                        continue
                    lines.append(line)
                    P_50_value, A_50_value = self.calc(
                        line,
                        ground_points,
                        dist_bipol,
                    )
                    A_50.append(A_50_value)
                    P_50.append(P_50_value)
        return p_50_sum(np.array(P_50)), list(zip(lines, A_50))


def p_50_sum(P_50: NDArray[np.float64]) -> NDArray[np.float64]:
    """Sum the audible noise from all lines for each ground point."""
    out: NDArray[np.float64] = 10.0 * np.log10(np.sum(10.0 ** (P_50 / 10.0), axis=0))
    return out


def altitude_correction(altitude: float) -> float:
    """Correction term for the altitude."""
    return (altitude - 300.0) / 300.0


def delta_rain_table_lookup(weather: Weather, rain_rate: float, _E: float, _line: Line) -> float:
    """Lookup the correction relative to a reference rain rate of `r_wc = 0.75mm/h` in a table."""
    if 0.0 < rain_rate <= 30.0 and weather == Weather.Foul:
        return raw_rain_correction(rain_rate)
    return 0.0


def delta_rain_table_lookup_plus_delta_A(
    weather: Weather, rain_rate: float, E: float, line: Line
) -> float:
    """Lookup the correction relative to a reference rain rate.

    Reference rate: `r_wc = 0.75mm/h` in a table adding the EPRI delta_A term.
    """
    d = line.con_radius * 2 * 100.0  # radius [m] -> diameter [cm]
    d_bundle = line.bundle_radius * 2 * 100.0  # radius [m] -> diameter [cm]
    return delta_rain_table_lookup(weather, rain_rate, E, line) + compute_delta_A(
        line.num_con, d, d_bundle, E
    )


T = TypeVar("T", bound=float | NDArray[np.float64])


def prepare_piecewise_const(graph: NDArray[np.float64], dx: float) -> Callable[[T], T]:
    """Prepare a piecewise constant function `f`.

    Prepare such that
    * `f(graph[:, 0]) = graph[:, 1]`,
    * `f` jumps at `(graph[i, 0] + graph[i+1, 0])/2` for i=0,...

    The implementation has lookup complexity of O(1).
    """
    x_jump, y = graph.T.copy()  # Copy to obtain memory contiguity for y
    x_middle = 0.5 * (x_jump[1:] + x_jump[:-1])
    x0 = x_middle[0]
    i_middle = np.round((x_middle - x0) / dx).astype(int)
    i_raster = np.arange(i_middle[0], i_middle[-1] + 2, dtype=int)
    y_raster = y[np.searchsorted(i_middle, i_raster)]

    def piecewise_const(x: T) -> T:
        index = (1 + np.floor((x - x0) / dx)).astype(int)
        y_out: T = y_raster[np.clip(index, 0, y_raster.size - 1)]
        return y_out

    return piecewise_const


# Rain rate correction (rain rate [mm/h], correction [dB(A)])
# relative to a reference of `r_wc = 0.75mm/h`:
raw_rain_correction = prepare_piecewise_const(
    np.array(
        [
            [0.1, -2.00],
            [0.2, -1.40],
            [0.3, -1.01],
            [0.4, -0.73],
            [0.5, -0.50],
            [0.6, -0.30],
            [0.7, -0.14],
            [0.75, 0.00],
            [0.8, 0.00],
            [0.9, 0.13],
            [1.0, 0.27],
            [1.1, 0.37],
            [1.2, 0.47],
            [1.3, 0.57],
            [1.4, 0.68],
            [1.5, 0.78],
            [1.6, 0.86],
            [1.7, 0.94],
            [1.8, 1.03],
            [1.9, 1.11],
            [2.0, 1.18],
            [2.1, 1.25],
            [2.2, 1.31],
            [2.3, 1.38],
            [2.4, 1.45],
            [2.5, 1.50],
            [2.6, 1.57],
            [2.7, 1.63],
            [2.8, 1.69],
            [2.9, 1.75],
            [3.0, 1.81],
            [3.5, 2.06],
            [4.0, 2.35],
            [4.5, 2.55],
            [5.0, 2.79],
            [5.5, 2.98],
            [6.0, 3.18],
            [6.5, 3.37],
            [7.0, 3.53],
            [7.5, 3.72],
            [7.7, 3.79],
            [8.0, 3.89],
            [8.5, 4.03],
            [9.0, 4.19],
            [9.5, 4.36],
            [10.0, 4.52],
            [11.0, 4.80],
            [12.0, 5.08],
            [13.0, 5.35],
            [14.0, 5.67],
            [15.0, 5.97],
            [16.0, 6.22],
            [17.0, 6.47],
            [18.0, 6.71],
            [19.0, 6.98],
            [20.0, 7.26],
            [21.0, 7.47],
            [22.0, 7.69],
            [23.0, 7.92],
            [24.0, 8.14],
            [25.0, 8.37],
            [26.0, 8.56],
            [27.0, 8.74],
            [28.0, 8.93],
            [29.0, 9.11],
            [30.0, 9.28],
        ]
    ),
    dx=0.025,
)


def season_dc_offset_bpa(season: Season) -> int:
    """Store the correction terms for the seasons according to BPA calculations.

    Reference: Formulas for Predicting Audible Noise from Overhead High Voltage AC and DC Lines
    by V. L. Chartier and R. D. Stearns
    published 1981 in IEEE Transactions on Power Apparatus and Systems
    page 128 / section "General DC Equation"
    """

    season_dict = {
        Season.Winter: -2,
        Season.Fall: 0,
        Season.Summer: 2,
        Season.Spring: 0,
    }
    return season_dict[season]


def season_dc_offset_epri(season: Season) -> int:
    """Store the correction terms for the seasons according to BPA calculations.

    Reference: Formulas for Predicting Audible Noise from Overhead High Voltage AC and DC Lines
    by V. L. Chartier and R. D. Stearns
    published 1981 in IEEE Transactions on Power Apparatus and Systems
    page 128 / section "General DC Equation"
    """

    season_dict = {
        Season.Winter: -4,
        Season.Fall: -2,
        Season.Summer: 0,
        Season.Spring: -2,
    }
    return season_dict[season]
