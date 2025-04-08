"""csv export."""

from __future__ import annotations

import csv
from typing import TYPE_CHECKING

import numpy as np

from hvlbuzz.config.config import Config, OffsetUnit
from hvlbuzz.physics.line import LineType

from .line_types import LINE_TYPES
from .settings_data_rows import settings_data_rows

if TYPE_CHECKING:
    from collections.abc import Iterable

    from hvlbuzz.core import ResultValues

BASE_HEADER = (
    "System",
    "Line",
    "X [m]",
    "Y [m]",
    "AC E-Field [kV/cm]",
    "DC E-Field [kV/cm]",
    "E_c [kV/cm]",
    "ΔA [dB]",
)


def table_header(L_names: list[str], sound_unit: OffsetUnit) -> tuple[str, ...]:
    """Assemble the table header from basic columns and sound columns."""
    if sound_unit == OffsetUnit.pw_m:
        unit_string = "dB/pW"
    elif sound_unit == OffsetUnit.w_m:
        unit_string = "dB/W"
    else:
        unit_string = "dB/?"

    return BASE_HEADER + tuple(f"{name} [{unit_string}]" for name in L_names)


def tabularize(
    result_values: ResultValues, *, group_coordinates: bool = False
) -> Iterable[list[str]]:
    """Tabularize result values.

    If `group_coordinates` is set to true, format `(x, y)` into a single cell.
    """

    line_values = result_values.sound.line_values
    for row in line_values:
        line = row.line
        try:
            e_ac, e_dc = f"{line.E_ac:.2f}", f"{line.E_dc:.2f}"
        except AttributeError:
            e_ac, e_dc = "", ""

        def fmt_a(value: float | None) -> str:
            return f"{value:.2f}" if value else "-"

        coordinates = (
            (f"({line.line_x}, {line.line_y})",)
            if group_coordinates
            else (str(line.line_x), str(line.line_y))
        )

        if line.line_type in (LineType.gnd, LineType.dc_neg, LineType.dc_pos, LineType.dc_neut):
            row.E_c = np.nan
            row.delta_A = np.nan

        yield [
            str(row.system_index),
            LINE_TYPES[line.line_type],  # line type
            *coordinates,
            e_ac,
            e_dc,
            f"{row.E_c:.2f}",
            f"{row.delta_A:.2f}",
            *(fmt_a(A) for A in row.A),
        ]


def export_csv(
    path: str, result_values: ResultValues, config: Config, loaded_json: str | None
) -> None:
    """Save the data of result values into a CSV file."""

    if not path.endswith(".csv"):
        path += ".csv"
    with open(path, "w", newline="", encoding="utf-8") as csvfile:
        delimiter = config.export.csv_delimiter.value
        dec_sep = config.export.csv_decimal.value

        writer = csv.writer(csvfile, delimiter=delimiter)
        settings_rows = settings_data_rows(str(loaded_json), config)
        writer.writerows(
            [
                ["Calculation Settings"],
                [],
                *settings_rows,
                [],
                ["Tower Configuration"],
                [],
            ]
        )

        for system in result_values.tower.systems:
            writer.writerows(
                [
                    [
                        "System Type:",
                        system.system_type.name.upper(),
                        "Voltage [kV]:",
                        f"{system.voltage / 1000:.2f}".replace(".", dec_sep),
                        "Current [kA]:",
                        f"{system.current / 1000:.3f}".replace(".", dec_sep),
                    ],
                    [
                        "Line Type",
                        "X-Coordinate [m]",
                        "Y-Coordinate [m]",
                        "No. of Conductors",
                        "Conductor Radius [mm]",
                        "Bundle Radius [mm]",
                        "Conductor Angle Offset [deg]",
                    ],
                ]
            )
            for line in system.lines:
                writer.writerow(
                    [
                        line.line_type.name,
                        f"{line.line_x:.2f}".replace(".", dec_sep),
                        f"{line.line_y:.2f}".replace(".", dec_sep),
                        line.num_con,
                        f"{line.con_radius * 1000:.2f}".replace(".", dec_sep),
                        f"{line.bundle_radius * 1000:.2f}".replace(".", dec_sep),
                        f"{line.con_angle_offset:.2f}".replace(".", dec_sep),
                    ]
                )
            writer.writerow([])

        # add audible noise plot data
        writer.writerows(
            [
                ["Audible Noise"],
                [],
                ["Surface Field Gradients and Generated Acoustic Power"],
                [],
            ]
        )

        L_names = result_values.sound.L_names()

        tab_header = list(
            table_header(
                L_names,
                config.sound.general_settings.an_unit,
            )
        )
        tab = [tab_header] + [
            [value.replace(".", dec_sep) for value in row] for row in tabularize(result_values)
        ]

        # write table data into csv file
        writer.writerows(tab)

        gp = ["Ground Points"] + [str(x).replace(".", dec_sep) for x in result_values.sound.x]
        sound_rows = [
            ["AN " + name] + [str(x).replace(".", dec_sep) for x in L]
            for name, L in zip(L_names, result_values.sound.L)
        ]

        writer.writerows(
            [[], ["Sound Pressure Level [dBA]"], [], gp, *sound_rows, []],
        )

        # add electric field plot data
        gp_e, height = zip(
            *(
                [("X-Coordinates", "Y-Coordinates")]
                + [
                    (
                        str(x).replace(".", dec_sep),
                        str(result_values.e_field.h).replace(".", dec_sep),
                    )
                    for x in result_values.e_field.x
                ]
            )
        )
        E_ac = ["AC Electric Field"] + [
            str(x).replace(".", dec_sep) for x in result_values.tower.E_ac_ground
        ]
        E_dc = ["DC Electric Field"] + [
            str(x).replace(".", dec_sep) for x in result_values.tower.E_dc_ground
        ]

        writer.writerows([["Electric Field [kV/m]"], gp_e, height, E_ac, E_dc, []])

        # add magnetic field plot data
        gp_b, height = zip(
            *(
                [("X-Coordinates", "Y-Coordinates")]
                + [
                    (
                        str(x).replace(".", dec_sep),
                        str(result_values.b_field.h).replace(".", dec_sep),
                    )
                    for x in result_values.b_field.x
                ]
            )
        )
        B_ac = ["AC Magnetic Field"] + [
            str(x).replace(".", dec_sep) for x in result_values.tower.B_ac
        ]
        B_dc = ["DC Magnetic Field"] + [
            str(x).replace(".", dec_sep) for x in result_values.tower.B_dc
        ]
        writer.writerows([["Magnetic Field [uT]"], gp_b, height, B_ac, B_dc])
