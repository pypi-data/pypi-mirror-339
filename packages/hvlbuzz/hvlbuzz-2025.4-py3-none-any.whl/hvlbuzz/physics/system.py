"""Physical model for a system."""

from collections.abc import Sequence
from enum import Enum, auto
from typing import Any

import numpy as np

from .line import Line


class SystemType(Enum):
    """Type of current used in the system."""

    ac = auto()
    dc = auto()
    dc_bipol = auto()
    gnd = auto()


class System:
    """Contains a collection of lines belonging to the same system.

    A system can have any of the following voltage signal form: AC, DC, GND.

    initialization varibale(s):

    * system_type: the current type
    * voltage: (rms phase-to-phase voltage for AC)

    The lines belonging to the system are collected in an array of objects.
    """

    def __init__(
        self,
        system_type: SystemType,
        voltage: float,
        current: float,
        lines: Sequence[Line] = (),
    ) -> None:
        # save input variables as object variables
        self.system_type = system_type
        self.voltage = voltage
        self.current = current

        # the lines array contain the line instances belonging to this system
        self.lines = list(lines)

    def add_line(self, line: Line) -> None:
        """This method adds a Line instance to the lines list."""
        self.lines.append(line)

    def get_system_type(self) -> str:
        """Return the system type as string in uppercase."""
        return self.system_type.name.upper()

    def get_voltage(self) -> str:
        """Return the voltage as string in the unit kV."""
        return str(self.voltage / 1000)

    def set_voltage(self, voltage: float) -> None:
        """This method sets the voltage of the system."""
        self.voltage = voltage

    def get_current(self) -> str:
        """Return the current as string in the unit kA."""
        return str(self.current / 1000)

    def set_current(self, current: float) -> None:
        """This method sets the current of the system."""
        self.current = current

    def get_num_con(self) -> str:
        """Return the number of conductor in lines if identical.

        The return value is a string.
        """
        num_con = [line.num_con for line in self.lines]
        if is_homogeneous_list(num_con):
            return str(num_con[0])
        return ""

    def set_num_con(self, num_con: int) -> None:
        """This method sets the number of conductor in a system bundle."""
        for line in self.lines:
            line.set_num_con(num_con)

    def get_con_radius(self) -> str:
        """Return the conductor radius in lines if identical.

        The return value is a string with the unit mm.
        """
        con_radius = [line.con_radius for line in self.lines]
        if is_homogeneous_list(con_radius):
            return str(con_radius[0] * 1000)
        return ""

    def get_con_diameter(self) -> str:
        """Return the conductor radius in lines if identical.

        The return value is a string with the unit mm.
        """
        con_radius = [line.con_radius for line in self.lines]
        if is_homogeneous_list(con_radius):
            return str(con_radius[0] * 2000)
        return ""

    def set_con_radius(self, con_radius: float) -> None:
        """This method sets the conductor radius of the system."""
        for line in self.lines:
            line.set_con_radius(con_radius)

    def get_bundle_radius(self) -> str:
        """Return the bundle radius in lines if identical.

        The return value is a string with the unit mm.
        """
        bundle_radius = [line.bundle_radius for line in self.lines]
        if is_homogeneous_list(bundle_radius):
            return str(bundle_radius[0] * 1000)
        return ""

    def get_bundle_spacing(self) -> str:
        """Return the bundle spcing in lines if identical.

        The return value is a string with the unit mm.
        """
        bundle_radius = [line.bundle_radius for line in self.lines]
        num_con = [line.num_con for line in self.lines]
        if is_homogeneous_list(bundle_radius) and is_homogeneous_list(num_con):
            radius = bundle_radius[0] * 1000
            n_poly = num_con[0]
            return f"{2 * radius * np.sin(np.pi / n_poly):.2f}".rstrip("0").rstrip(".")
        return ""

    def set_bundle_radius(self, bundle_radius: float) -> None:
        """This method sets the bundle radius of the system."""
        for line in self.lines:
            line.set_bundle_radius(bundle_radius)

    def get_con_angle_offset(self) -> str:
        """Return the conductor angle offset in lines if identical.

        The return value is a string in the unit degrees.
        """
        con_angle_offset = [line.con_angle_offset for line in self.lines]
        if is_homogeneous_list(con_angle_offset):
            return str(con_angle_offset[0])
        return ""

    def set_con_angle_offset(self, con_angle_offset: float) -> None:
        """This method sets the conductor angle offset of the system."""
        for line in self.lines:
            line.set_con_angle_offset(con_angle_offset)


def is_homogeneous_list(lst: list[Any]) -> bool:
    """This is a utility method that checks if all elements are equal."""
    if not lst:
        return True
    return [lst[0]] * len(lst) == lst
