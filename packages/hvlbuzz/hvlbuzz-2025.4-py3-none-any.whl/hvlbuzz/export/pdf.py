"""pdf export."""

from __future__ import annotations

import os
from tempfile import TemporaryDirectory
from typing import TYPE_CHECKING

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle

from hvlbuzz.config.ini import serialize_enum

from .csv import tabularize
from .settings_data_rows import settings_data_rows

if TYPE_CHECKING:
    import matplotlib.figure

    from hvlbuzz.config.config import Config
    from hvlbuzz.core import ResultValues
    from hvlbuzz.physics.system import System


def export_pdf(  # noqa: PLR0913
    path: str,
    result_values: ResultValues,
    config: Config,
    loaded_json: str | None,
    sound_fig: matplotlib.figure.Figure,
    e_fig: matplotlib.figure.Figure,
    b_fig: matplotlib.figure.Figure,
) -> None:
    """Creates a PDF file with current plots and table.

    input variable(s):

    * path: the directory path to save the PDF file in
    * filename: the filename of the PDF file
    """

    systems = result_values.tower.systems
    # create a temporary path for PNG images
    with TemporaryDirectory() as temp_path:  # Ensures cleanup
        # save audible image plot as PNG image
        an_img = create_image(temp_path, "Audible Noise", sound_fig)
        # save electric field plot as PNG image
        ef_img = create_image(temp_path, "Electric Field", e_fig)
        # save magnetic field plot as PNG image
        mf_img = create_image(temp_path, "Magnetic Field", b_fig)

        # create a PDF file
        if not path.endswith(".pdf"):
            path += ".pdf"
        c = canvas.Canvas(path, pagesize=A4)

        # get page sizes
        width, height = A4
        yspace = (height - width) / 4

        settings_data = [["Settings", "Values"], *settings_data_rows(loaded_json or "", config)]

        # define table styling
        settings_table = Table(
            settings_data,
            2 * [40 * mm],
            len(settings_data) * [7 * mm],
            style=TableStyle(
                [
                    ("FONTSIZE", (0, 0), (-1, -1), 7),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.black),
                    ("BOX", (0, 0), (-1, -1), 0.25, colors.black),
                    ("BACKGROUND", (0, 0), (-1, 0), colors.black),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ]
            ),
        )

        # draw table on the bottom of first page
        settings_table.wrapOn(c, width, height)
        settings_table.drawOn(c, width / 2 - 40 * mm, height / 2 + 2 * yspace)

        # newpage
        c.showPage()  # added because sometimes config_table would overlap with settings_table

        config_data = []
        for system in systems:
            config_data += system_geometry_data(system)

        # define table styling
        config_table = Table(
            config_data,
            7 * [20 * mm],
            len(config_data) * [7 * mm],
            style=TableStyle(
                [
                    ("FONTSIZE", (0, 0), (-1, -1), 7),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.black),
                    ("BOX", (0, 0), (-1, -1), 0.25, colors.black),
                ]
            ),
        )

        # draw table on the bottom of first page
        config_table.wrapOn(c, width, height)
        config_table.drawOn(c, width / 2 - 70 * mm, yspace)

        # end the first page
        c.showPage()

        # insert audible noise table headers
        sound_header = result_values.sound.L_names()
        sound_unit = "in " + serialize_enum(config.sound.general_settings.an_unit)
        headers, col_widths, units = zip(
            *(
                ("System", 10.0 * mm, ""),
                ("Line", 10.0 * mm, ""),
                ("Coordinates", 15.0 * mm, "in m"),
                ("AC E-Field", 12.0 * mm, "in kV/cm"),
                ("DC E-Field", 12.0 * mm, "in kV/cm"),
                ("E_c", 10.0 * mm, "in kV/cm"),
                ("ΔA", 10.0 * mm, "in dB"),
                *((s, 22.0 * mm, sound_unit) for s in sound_header),
            ),
            strict=True,
        )
        sound_data = [
            headers,
            units,
            *tabularize(result_values, group_coordinates=True),
        ]
        # define table styling
        sound_table = Table(
            sound_data,
            col_widths,
            style=TableStyle(
                [
                    ("FONTSIZE", (0, 0), (-1, -1), 7),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.black),
                    ("BOX", (0, 0), (-1, -1), 0.25, colors.black),
                    ("BACKGROUND", (0, 0), (-1, 0), colors.black),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ]
            ),
        )

        # draw table on the bottom of first page
        sound_table.wrapOn(c, width, height)
        sound_table.drawOn(c, 3.75 * mm, yspace)

        # draw audible noise image of top of first page
        c.drawImage(an_img, width / 4, height / 2, width=width / 2, height=width / 2)

        # end the second page
        c.showPage()

        # draw the electric field image on the left of second page
        c.drawImage(ef_img, 0, width / 2, width=width / 2, height=width / 2)
        # draw the magnetic field image on the right of first page
        c.drawImage(mf_img, width / 2, width / 2, width=width / 2, height=width / 2)

        # end the third page
        c.showPage()

        #  save the PDF file
        c.save()


def create_image(tmp_dir: str, caption: str, fig: matplotlib.figure.Figure) -> ImageReader:
    """Draw an image of a plot in memory (via a temp file)."""
    filename = caption.replace(" ", "").lower() + ".png"
    path = os.path.join(tmp_dir, filename)
    # set the size of the image for better quality
    fig.set_size_inches(7, 7)
    fig.savefig(path)
    return ImageReader(path)


def system_geometry_data(system: System) -> list[list[str]]:
    """Assemble info about the geometry of a system in table format (nested list of strings)."""
    return [
        [
            "System Type:",
            system.system_type.name.upper(),
            "Voltage [kV]:",
            f"{system.voltage / 1000:.2f}",
            "Current [kA]:",
            f"{system.current / 1000:.3f}",
            "",
        ],
        [
            "Line Type",
            "X-Coord [m]",
            "Y-Coord [m]",
            "# Conductors",
            "r_con [mm]",
            "r_bundle [mm]",
            "alpha [°]",
        ],
        *(
            [
                line.line_type.name,
                f"{line.line_x:.2f}",
                f"{line.line_y:.2f}",
                str(line.num_con),
                f"{line.con_radius * 1000:.2f}",
                f"{line.bundle_radius * 1000:.2f}",
                f"{line.con_angle_offset:.2f}",
            ]
            for line in system.lines
        ),
        ["", "", "", "", "", "", ""],
    ]
