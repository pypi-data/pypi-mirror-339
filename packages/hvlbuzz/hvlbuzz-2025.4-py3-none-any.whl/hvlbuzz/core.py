"""Top level logic."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

import numpy as np

from .physics import sound
from .physics.system import System, SystemType

if TYPE_CHECKING:
    from collections.abc import Callable

    from numpy.typing import NDArray

    from .config.config import (
        Config,
        ElectricFieldGroundPoints,
        MagneticFieldGroundPoints,
        SoundConfig,
        SoundGroundPoints,
    )
    from .physics.line import Line
    from .physics.tower import Tower


@dataclass
class SoundPlot:
    """Declaration of a plot of a sound routine."""

    name: str
    color: str
    run_routine: Callable[
        [list[System], NDArray[np.float64], SoundConfig],
        tuple[NDArray[np.float64], list[tuple[Line, float]]],
    ]
    enabled: Callable[[SoundConfig], bool]


@dataclass
class EFieldValues:
    """Result values of a E field calculation."""

    x: NDArray[np.float64] = field(default_factory=lambda: np.array([]))
    """Ground sampling points for the cross sectional profile of the E field."""
    h: float = 0.0
    """Height over ground which has been in use when the result was computed."""


@dataclass
class BFieldValues:
    """Result values of a B field calculation."""

    x: NDArray[np.float64] = field(default_factory=lambda: np.array([]))
    """Ground sampling points for the cross sectional profile of the B field."""
    h: float = 0.0
    """Height over ground which has been in use when the result was computed."""


@dataclass
class LineValues:
    """Result values per line."""

    line: Line
    """Line for which the values have been computed."""
    system_index: int
    """Index of the system of the line."""
    E_c: float
    delta_A: float
    """Correction heavy rain (6.5mm/h) -> wet conductor (0.75mm/h)."""
    A: NDArray[np.float64]
    """Sound level values per routine."""

    @classmethod
    def from_line(cls, line: Line, system_index: int, n_routines: int) -> LineValues:
        """Create an instance from a line."""
        n = line.num_con
        d = line.con_radius * 2 * 100
        d_b = line.bundle_radius * 2 * 100
        E_c = sound.compute_E_c(n, d)
        delta_A = sound.compute_delta_A_from_E_c(n, d, d_b, line.E_ac, E_c)
        return cls(line, system_index, E_c, delta_A, np.full(n_routines, np.nan))


@dataclass
class SoundLevelValues:
    """Result values of a sound calculation."""

    x: NDArray[np.float64] = field(default_factory=lambda: np.array([]))
    """Ground sampling points for the cross sectional profile of the sound levels."""
    L: NDArray[np.float64] = field(default_factory=lambda: np.array([]))
    """Sound level values for the cross sectional profile for each selected routine.
    Shape: (n_routines, n_sampling_points)"""
    plots: list[SoundPlot] = field(default_factory=list)
    """Selected sound routines with their plot parameters."""
    line_values: list[LineValues] = field(default_factory=list)
    """Result values per line."""

    def L_names(self) -> list[str]:
        """Names of all sound routines in use."""
        return [p.name for p in self.plots]


@dataclass
class ResultValues:
    """Result values of a hvlbuzz calculation."""

    tower: Tower
    """Tower instance which calculates the plot data"""
    sound: SoundLevelValues = field(default_factory=SoundLevelValues)
    e_field: EFieldValues = field(default_factory=EFieldValues)
    b_field: BFieldValues = field(default_factory=BFieldValues)


def compute_e_cross_section(tower: Tower, config: Config) -> EFieldValues:
    """For given config, calculate the cross sectional profile of the E field."""
    x = sample_ground_points(config.electric_field.ground_points)
    h = config.electric_field.ground_points.height_above_ground
    # get the number of contour points
    tower.num_contour = config.electric_field.general_config.num_contour
    # calculate the electric field
    if not tower.calc_electric_field(x, h):
        msg = "Line Collision: ground electric field calculation aborted."
        raise RuntimeError(msg)
    return EFieldValues(x, h)


def compute_b_cross_section(tower: Tower, config: Config) -> BFieldValues:
    """For given config, calculate the cross sectional profile of the B field."""
    x = sample_ground_points(config.magnetic_field.ground_points)
    h = config.magnetic_field.ground_points.height_above_ground
    # calculate the electric field
    if not tower.calc_magnetic_field(x, h):
        msg = "Line Collision: ground magnetic field calculation aborted."
        raise RuntimeError(msg)
    return BFieldValues(x, h)


def compute_sound(tower: Tower, config: Config) -> SoundLevelValues:
    """Compute the audible noise levels according to the available routines."""
    plots = []
    system_types = {system.system_type for system in tower.systems}

    if SystemType.ac in system_types:
        plots += list(AC_PLOTS)
    if SystemType.dc in system_types or SystemType.dc_bipol in system_types:
        plots += list(DC_PLOTS)

    plots = [plot for plot in plots if plot.enabled(config.sound)]
    return compute_sound_for_routines(tower, config, plots)


def compute_sound_for_routines(
    tower: Tower, config: Config, routines: list[SoundPlot]
) -> SoundLevelValues:
    """Compute the audible noise levels according to the available routines."""
    x_ground_points = sample_ground_points(config.sound.ground_points)
    # get the number of contour points
    tower.num_contour = config.electric_field.general_config.num_contour
    # calculate the conductor surface gradient
    if not tower.calc_ave_max_conductor_surface_gradient():
        msg = "Line Collision: surface gradient calculation aborted."
        raise RuntimeError(msg)

    level_unit = config.sound.general_settings.an_unit.value
    ground_points = np.vstack(
        (
            x_ground_points,
            np.full_like(x_ground_points, config.sound.ground_points.height_above_ground),
        )
    )

    L = np.empty((len(routines), x_ground_points.size))
    line_values = {
        id(line): LineValues.from_line(line, sys_idx, len(routines))
        for sys_idx, system in enumerate(tower.systems, start=1)
        for line in system.lines
    }
    for n, (plot, l_row) in enumerate(zip(routines, L)):
        l_row[()], A_by_line = plot.run_routine(tower.systems, ground_points, config.sound)
        for line, A in A_by_line:
            line_values[id(line)].A[n] = A + level_unit

    return SoundLevelValues(
        x=x_ground_points, L=L, plots=routines, line_values=list(line_values.values())
    )


def calc_ac(
    from_config: Callable[[SoundConfig], tuple[sound.AcSoundRoutineParameters, bool]],
) -> Callable[
    [list[System], NDArray[np.float64], SoundConfig],
    tuple[NDArray[np.float64], list[tuple[Line, float]]],
]:
    """Prepare a function calculating the sound levels for a given config extractor `from_config`.

    The returned function can be used as the `run_routine` field of `SoundPlot`.
    """

    def calc(
        systems: list[System], ground_points: NDArray[np.float64], sound_config: SoundConfig
    ) -> tuple[NDArray[np.float64], list[tuple[Line, float]]]:
        parametrized_routine, offset = from_config(sound_config)
        return calc_ac_sound_routine(
            systems, ground_points, offset=offset, parametrized_routine=parametrized_routine
        )

    return calc


def calc_ac_sound_routine(
    systems: list[System],
    ground_points: NDArray[np.float64],
    parametrized_routine: sound.AcSoundRoutineParameters,
    *,
    offset: bool,
) -> tuple[NDArray[np.float64], list[tuple[Line, float]]]:
    """Calculate the audible noise level for the given AC routine and parameters."""
    calc = (
        parametrized_routine.calc_systems
        if not offset
        else parametrized_routine.calc_systems_offset
    )
    return calc(systems, ground_points)


def ac_epri_config(sound_config: SoundConfig) -> tuple[sound.AcSoundRoutineParameters, bool]:
    """Extract config values for a `sound.AcSoundRoutineParameters` instance for `sound.AcEpri`."""
    return (
        sound.AcEpri(
            weather=sound_config.ac_epri.weather,
            rain_rate=sound_config.general_settings.ac_rain_intensity,
            altitude=sound_config.general_settings.altitude,
            use_efield_independent_rain_correction=sound_config.ac_epri.use_efield_independent_rain_correction,
        ),
        sound_config.ac_epri.offset,
    )


def ac_bpa_config(sound_config: SoundConfig) -> tuple[sound.AcSoundRoutineParameters, bool]:
    """Extract config values for a `sound.AcSoundRoutineParameters` instance for `sound.AcBpa`."""
    return (
        sound.AcBpa(
            weather=sound_config.ac_bpa.weather,
            rain_rate=sound_config.general_settings.ac_rain_intensity,
            altitude=sound_config.general_settings.altitude,
            use_efield_independent_rain_correction=sound_config.ac_bpa.use_efield_independent_rain_correction,
        ),
        sound_config.ac_bpa.offset,
    )


def ac_bpa_mod_config(sound_config: SoundConfig) -> tuple[sound.AcSoundRoutineParameters, bool]:
    """Extract config values for `sound.AcBpaMod`."""
    return (
        sound.AcBpaMod(
            weather=sound_config.ac_bpa_mod.weather,
            rain_rate=sound_config.general_settings.ac_rain_intensity,
            altitude=sound_config.general_settings.altitude,
        ),
        sound_config.ac_bpa_mod.offset,
    )


def ac_edf_config(sound_config: SoundConfig) -> tuple[sound.AcSoundRoutineParameters, bool]:
    """Extract config values for a `sound.AcSoundRoutineParameters` instance for `sound.AcEdf`."""
    return (
        sound.AcEdf(
            rain_rate=sound_config.general_settings.ac_rain_intensity,
            altitude=sound_config.general_settings.altitude,
        ),
        sound_config.ac_edf.offset,
    )


def calc_dc(
    from_config: Callable[[SoundConfig], sound.DcSoundRoutineParametersBase],
) -> Callable[
    [list[System], NDArray[np.float64], SoundConfig],
    tuple[NDArray[np.float64], list[tuple[Line, float]]],
]:
    """Prepare a function calculating the sound levels for a given config extractor `from_config`.

    The returned function can be used as the `run_routine` field of `SoundPlot`.
    """

    def calc(
        systems: list[System], ground_points: NDArray[np.float64], sound_config: SoundConfig
    ) -> tuple[NDArray[np.float64], list[tuple[Line, float]]]:
        parametrized_routine = from_config(sound_config)
        return parametrized_routine.calc_systems(systems, ground_points)

    return calc


def dc_epri_config(sound_config: SoundConfig) -> sound.DcSoundRoutineParametersBase:
    """Extract config values for `sound.DcEpri`."""
    return sound.DcEpri(
        weather=sound_config.dc_epri.weather,
        season=sound_config.dc_epri.season,
        altitude=sound_config.general_settings.altitude,
    )


def dc_bpa_config(sound_config: SoundConfig) -> sound.DcSoundRoutineParametersBase:
    """Extract config values for `sound.DcBpa`."""
    return sound.DcBpa(
        weather=sound_config.dc_bpa.weather,
        season=sound_config.dc_bpa.season,
        altitude=sound_config.general_settings.altitude,
    )


def dc_criepi_config(_sound_config: SoundConfig) -> sound.DcSoundRoutineParametersBase:
    """Extract config values for `sound.DcCriepi`."""
    return sound.DcCriepi()


def sample_ground_points(
    config: SoundGroundPoints | ElectricFieldGroundPoints | MagneticFieldGroundPoints,
) -> NDArray[np.float64]:
    """Create equispaced ground points based on the config."""
    return np.linspace(
        config.ground_points_start,
        config.ground_points_end,
        num=config.ground_points_n,
    )


AC_PLOTS = (
    SoundPlot(
        name=sound.AcEpri.name,
        color="midnightblue",
        run_routine=calc_ac(ac_epri_config),
        enabled=lambda cfg: cfg.ac_epri.enabled,
    ),
    SoundPlot(
        name=sound.AcBpa.name,
        color="blue",
        run_routine=calc_ac(ac_bpa_config),
        enabled=lambda cfg: cfg.ac_bpa.enabled,
    ),
    SoundPlot(
        name=sound.AcBpaMod.name,
        color="cornflowerblue",
        run_routine=calc_ac(ac_bpa_mod_config),
        enabled=lambda cfg: cfg.ac_bpa_mod.enabled,
    ),
    SoundPlot(
        name=sound.AcEdf.name,
        color="lightseagreen",
        run_routine=calc_ac(ac_edf_config),
        enabled=lambda cfg: cfg.ac_edf.enabled,
    ),
)
DC_PLOTS = (
    SoundPlot(
        name=sound.DcEpri.name,
        color="firebrick",
        run_routine=calc_dc(dc_epri_config),
        enabled=lambda cfg: cfg.dc_epri.enabled,
    ),
    SoundPlot(
        name=sound.DcBpa.name,
        color="orangered",
        run_routine=calc_dc(dc_bpa_config),
        enabled=lambda cfg: cfg.dc_bpa.enabled,
    ),
    SoundPlot(
        name=sound.DcCriepi.name,
        color="darkorange",
        run_routine=calc_dc(dc_criepi_config),
        enabled=lambda cfg: cfg.dc_criepi.enabled,
    ),
)
