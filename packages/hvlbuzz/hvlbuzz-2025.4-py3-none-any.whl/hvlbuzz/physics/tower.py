"""Physical model for a tower."""

import json
from collections.abc import Sequence
from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from .line import Line, LineType
from .system import System, SystemType

# Vacuum permittivity constant [F/m]
EPSILON_0 = 8.8541878128e-12
# Vacuum permeability [H/m]
MU_0 = 1.25663706212e-6

C_EPS = 1.0 / (2.0 * np.pi * EPSILON_0)


@dataclass
class Positions:
    """Contour and charge positions as well as unit vectors from conductors on a tower.

    Required for the electric field calculations.
    """

    contours: NDArray[np.float64]
    charges: NDArray[np.float64]
    mirror_charges: NDArray[np.float64]
    unit_vec: NDArray[np.float64]


class Tower:
    """Contains the geometrical information of the high voltage line systems in a list.

    Based on this information, the class methods can
    perform the following calculations:

    * Electric field on ground level
    * Magnetic field on ground level
    * Surface gradient on the conductors

    The Charge Simulation Method (CSM) is used for the electric field
    calculations. Thus, before the calculation of the electric field and surface
    gradient is performed, the electric field calculation accuracy must be set
    so that the Conductor instances can calculate the number of contour
    points needed for the calculation.
    """

    def __init__(self, systems: Sequence[System] = (), num_contour: int = 0) -> None:
        self.systems: list[System] = list(systems)
        self.num_contour = num_contour
        self.B_ac = np.array([])
        self.B_dc = np.array([])
        self.B_sum = np.array([])
        self.E_ac_ground = np.array([])
        self.E_dc_ground = np.array([])
        self.E_sum_ground = np.array([])
        self.E_ac = np.array([])
        self.E_dc = np.array([])

    def add_system(self, system: System) -> list[int]:
        """Check for line collisions between lines in the existing systems and the new system.

        If there are no line collision, the new system is added to the systems list.
        """

        line_idx = []
        for old_system in self.systems:
            for old_line in old_system.lines:
                old_coord = np.array([old_line.line_x, old_line.line_y])
                old_bundle_radius = old_line.bundle_radius
                for new_line_idx, new_line in enumerate(system.lines):
                    new_coord = np.array([new_line.line_x, new_line.line_y])
                    new_bundle_radius = new_line.bundle_radius

                    # calculate the difference between distance between lines
                    # and the sum of the bundle radius of both lines
                    dist = np.linalg.norm(new_coord - old_coord)
                    sum_bundle_radius = new_bundle_radius + old_bundle_radius
                    diff = dist - sum_bundle_radius

                    # if the difference is less than zero, there is line
                    # collision. save the line index of the colliding new line.
                    if diff < 0:
                        line_idx.append(new_line_idx)

        # add the new system if there is no collision (line_idx is empty)
        if not line_idx:
            self.systems.append(system)

        return line_idx

    def remove_system(self, system_index: int) -> None:
        """Remove the system on the system_index place in the systems list."""
        del self.systems[system_index]

    def reset_systems(self) -> None:
        """This method empties the systems list."""
        self.systems = []

    def calc_magnetic_field(
        self, ground_points: NDArray[np.float64], height_above_ground: float
    ) -> bool:
        """Compute the magnetic field on the ground level below the high voltage line conductors.

        The Biot-Savart formula is implemented here for the calculation of magnetic field.

        :param ground_points: Numpy array containing x-coordinates of ground points
        :param height_above_ground: height of ground points

        The calculation will be saved as class variable:

        * B_ac: magnetic field caused by AC conductors [1e-6 T]
        * B_dc: magnetic field caused by DC conductors [1e-6 T]

        The return value is a boolean status signaling the success of the
        calculation:

        * False: calculation aborted
        * True: calculation successful
        """

        # check for line collision
        if self._check_line_collision():
            return False

        # ground points coordinates
        ground_coords = np.column_stack(
            (ground_points, np.full(ground_points.shape, height_above_ground))
        )

        # conductor coordinates:
        cons = np.array(
            [
                [c.con_x, c.con_y]
                for system in self.systems
                for line in system.lines
                for c in line.cons
            ]
        )

        # shape: (n_conductors, n_ground_points, 2):
        diff = ground_coords - cons[:, None, :]
        diff_x = diff[..., 0]
        diff_y = diff[..., 1]
        dist_sq = (diff**2).sum(axis=2)
        denominator = dist_sq * 2 * np.pi
        v_x = -diff_y / denominator
        v_y = diff_x / denominator

        # get the conductor currents
        I_ac, I_dc = self.calc_currents()

        # calculate the AC magnetic field
        H_ac_x = I_ac @ v_x
        H_ac_y = I_ac @ v_y
        H_ac = np.hypot(np.abs(H_ac_x), np.abs(H_ac_y))
        # save the magnetic field in the correct unit [1e-6 T]
        self.B_ac = MU_0 * H_ac * 1000000.0

        # calculate the DC magnetic field
        H_dc_x = I_dc @ v_x
        H_dc_y = I_dc @ v_y
        H_dc = np.hypot(H_dc_x, H_dc_y)
        # save the magnetic field in the correct unit [1e-6 T]
        self.B_dc = MU_0 * H_dc * 1000000.0

        # save the sum of the magnetic fields
        self.B_sum = np.hypot(self.B_ac, self.B_dc)

        # return True if calculation is successful
        return True

    def calc_currents(self) -> tuple[NDArray[np.complex128], NDArray[np.float64]]:
        """Compute the AC and DC conductor currents for the magnetic field computation.

        Used in calc_magnetic_field.
        """

        angle_by_line_type = {
            LineType.ac_s: -2.0 * np.pi / 3,
            LineType.ac_t: -4.0 * np.pi / 3,
        }
        I_ac = []
        I_dc = []
        for system in self.systems:
            for line in system.lines:
                for _con in line.cons:
                    # handle AC currents using phasors
                    if system.system_type == SystemType.ac:
                        theta = angle_by_line_type.get(line.line_type, 0.0)
                        I_ac.append(system.current / line.num_con * np.exp(1j * theta))
                        I_dc.append(0.0)

                    # handle DC currents
                    elif system.system_type in {SystemType.dc, SystemType.dc_bipol}:
                        if line.line_type == LineType.dc_pos:
                            I_dc.append(system.current / line.num_con)
                        elif line.line_type == LineType.dc_neg:
                            I_dc.append(-system.current / line.num_con)
                        elif line.line_type == LineType.dc_neut:
                            I_dc.append(0.0)
                        I_ac.append(0.0)

                    # set currents of ground lines to zero
                    elif system.system_type == SystemType.gnd:
                        I_ac.append(0.0)
                        I_dc.append(0.0)

        return np.array(I_ac), np.array(I_dc)

    def calc_electric_field(
        self, ground_points: NDArray[np.float64], height_above_ground: float
    ) -> bool:
        """Compute the electric field on the ground level below the high voltage line conductors.

        The Charge Simulation Method (CSM) is used for the calculation of electric field.

        :param ground_points: Numpy array containing x-coordinates of ground points
        :param height_above_ground: height of ground points

        The calculation will be saved as class variable:

        * E_ac_ground: electric field caused by AC conductors [kV/cm]
        * E_dc_ground: electric field caused by DC conductors [kV/cm]

        The return value is a boolean status signaling the success of the
        calculation:

        * False: calculation aborted
        * True: calculation successful
        """

        # check for line collision
        if self._check_line_collision():
            return False

        # get the coordinates of contours, charges and mirror charges
        points = self.prepare_positions()
        contours = points.contours
        charges = points.charges
        mirror_charges = points.mirror_charges

        # create the array of ground points coordinates
        ground_coords = np.column_stack(
            (ground_points, np.full(ground_points.shape, height_above_ground))
        )

        # calculate the difference between contour points and each of
        # simulated charges points and mirror charge points
        # shape: (n_ground_coords, n_charges, 2):
        charges_diff = ground_coords[:, None, :] - charges
        mirror_charges_diff = ground_coords[:, None, :] - mirror_charges

        # split the difference into x- and y-coordinates
        charges_diff_x = charges_diff[..., 0]
        charges_diff_y = charges_diff[..., 1]

        mirror_charges_diff_x = mirror_charges_diff[..., 0]
        mirror_charges_diff_y = mirror_charges_diff[..., 1]

        # calculate the squares of the euclidean distances
        charges_norm_square = (charges_diff**2).sum(axis=2)
        mirror_charges_norm_square = (mirror_charges_diff**2).sum(axis=2)

        # calculate the x- and y-components of the v matrix
        gp_v_x = (
            charges_diff_x / charges_norm_square
            - mirror_charges_diff_x / mirror_charges_norm_square
        )
        gp_v_y = (
            charges_diff_y / charges_norm_square
            - mirror_charges_diff_y / mirror_charges_norm_square
        )

        # calculate the matrices
        pot_matrix, *_ = self.calc_matrices(contours, charges, mirror_charges)

        # calculate voltages
        U_ac, U_dc = self.calc_voltages()

        pot_inv = np.linalg.inv(pot_matrix)
        # calculate the AC electric field on ground
        line_charges_ac = pot_inv @ U_ac
        E_ac_x_ground = np.abs(gp_v_x @ line_charges_ac)
        E_ac_y_ground = np.abs(gp_v_y @ line_charges_ac)
        # save the electric field in the correct unit [kV/m]
        self.E_ac_ground = C_EPS * np.hypot(E_ac_x_ground, E_ac_y_ground) / 1000

        # calculate the DC electric field on ground
        line_charges_dc = pot_inv @ U_dc
        E_dc_x_ground = gp_v_x @ line_charges_dc
        E_dc_y_ground = gp_v_y @ line_charges_dc
        # save the electric field in the correct unit [kV/m]
        self.E_dc_ground = C_EPS * np.hypot(E_dc_x_ground, E_dc_y_ground) / 1000

        # calculate sum of electric fields
        self.E_sum_ground = np.hypot(self.E_ac_ground, self.E_dc_ground)

        # return True if the calculation is successful
        return True

    def calc_conductor_surface_gradient(self) -> bool:
        """Compute the surface gradients for all conductors on the tower.

        The Charge Simulation Method (CSM) is used for the calculation
        of electric field.

        The calculation will be saved as class variable:

        * E_ac: surface gradient caused by charges in AC conductors [kV/cm]
        * E_dc: surface gradient caused by charges in DC conductors [kV/cm]

        The return value is a boolean status signaling the success of the
        calculation:

        * False: calculation aborted
        * True: calculation successful
        """

        # check for line collision
        if self._check_line_collision():
            return False

        # get the coordinates of contours, charges and mirror charges
        points = self.prepare_positions()
        contours = points.contours
        charges = points.charges
        mirror_charges = points.mirror_charges
        unit_vec = points.unit_vec

        # split unit vectors into x- and y-components
        unit_vec_x, unit_vec_y = unit_vec.T

        # calculate voltages
        U_ac, U_dc = self.calc_voltages()

        # calculate the matrices
        pot_matrix, v_x, v_y = self.calc_matrices(contours, charges, mirror_charges)

        # calculate the AC and DC line charges.
        # Solving 2 systems simultaneously seems to be a bit more performant here
        # than inverting the matrix
        U: NDArray[np.complex128] = np.column_stack((U_ac, U_dc))
        line_charges_ac, line_charges_dc = np.linalg.solve(pot_matrix, U).T
        # calculate the x and y components of the DC electric field
        E_ac_x = v_x @ np.abs(line_charges_ac)
        E_ac_y = v_y @ np.abs(line_charges_ac)
        # multiply the x and y components with the corresponding unit vectors
        # and summing both terms
        self.E_ac = C_EPS * (E_ac_x * unit_vec_x + E_ac_y * unit_vec_y)

        # calculate the x and y components of the DC electric field
        E_dc_x = v_x @ np.real(line_charges_dc)
        E_dc_y = v_y @ np.real(line_charges_dc)
        # multiply the x and y components with the corresponding unit vectors
        # and summing both terms
        self.E_dc = C_EPS * (E_dc_x * unit_vec_x + E_dc_y * unit_vec_y)

        # return True of the calculation is successful
        return True

    def prepare_positions(self) -> Positions:
        """Prepare contour / charge positions and the unit vectors for all conductors on the tower.

        These positions are required for the electric field calculations.
        The number of contour positions in each conductor is determined by
        the calculation accuracy (calc_acc).
        """
        contours = []
        charges = []
        mirror_charges = []
        unit_vec = []

        def collect_xy(c: list[dict[str, float]]) -> list[list[float]]:
            return [[val["x"], val["y"]] for val in c]

        for system in self.systems:
            for line in system.lines:
                for con in line.cons:
                    # prompt the conductors to calculate the contour
                    # points accoding to  the calc_acc value of the tower.
                    con.set_points(line.con_radius, self.num_contour)
                    contours.extend(collect_xy(con.contours))
                    charges.extend(collect_xy(con.charges))
                    mirror_charges.extend(collect_xy(con.mirror_charges))
                    unit_vec.extend(collect_xy(con.unit_vec))

        # return the lists of coordinates in a dict
        return Positions(
            contours=np.array(contours),
            charges=np.array(charges),
            mirror_charges=np.array(mirror_charges),
            unit_vec=np.array(unit_vec),
        )

    def calc_voltages(self) -> tuple[NDArray[np.complex128], NDArray[np.float64]]:
        """Compute the conductor voltages which are required for the electric field calculations.

        Returns a tuple of AC voltages and DC voltages.
        """

        theta = {LineType.ac_r: 0.0, LineType.ac_s: -2 * np.pi / 3, LineType.ac_t: -4 * np.pi / 3}
        v_sign = {LineType.dc_pos: 1.0, LineType.dc_neut: 0.0, LineType.dc_neg: -1.0}

        U_ac = []
        U_dc = []
        for system in self.systems:
            for line in system.lines:
                for con in line.cons:
                    for _contour in con.contours:
                        # handle the AC conductor voltages
                        if system.system_type == SystemType.ac:
                            voltage = (
                                system.voltage / np.sqrt(3) * np.exp(1j * theta[line.line_type])
                            )
                            U_ac.append(voltage)
                            U_dc.append(0.0)

                        # handle the DC conductor voltages
                        elif system.system_type in {SystemType.dc, SystemType.dc_bipol}:
                            voltage = v_sign[line.line_type] * system.voltage
                            U_ac.append(0.0)
                            U_dc.append(voltage)

                        # set the voltages of ground lines to zero
                        elif system.system_type == SystemType.gnd:
                            U_ac.append(0.0)
                            U_dc.append(0.0)

        return np.array(U_ac), np.array(U_dc)

    def calc_matrices(
        self,
        contours: NDArray[np.float64],
        charges: NDArray[np.float64],
        mirror_charges: NDArray[np.float64],
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Compute the potential and v matrices required for the electric field calculation.

        :param contours: coordinates of contour points in a list
        :param charges: coordinates of charges points in a list
        :param mirror_charges: coordinates of mirror_charges points in a list

        :returns: A tuple consisting of the potential, the v_x and v_y matrices.
        """

        # calculate the difference between contour points and each of
        # simulated charges points and mirror charge points
        # shape: (n_ground_coords, n_charges, 2):
        charges_diff = contours[:, None, :] - charges
        mirror_charges_diff = contours[:, None, :] - mirror_charges

        # split the difference into x- and y-coordinates
        charges_diff_x = charges_diff[..., 0]
        charges_diff_y = charges_diff[..., 1]

        mirror_charges_diff_x = mirror_charges_diff[..., 0]
        mirror_charges_diff_y = mirror_charges_diff[..., 1]

        # calculate the euclidean distances
        charges_norm = np.linalg.norm(charges_diff, axis=2)
        mirror_charges_norm = np.linalg.norm(mirror_charges_diff, axis=2)

        # calculate the squares of the euclidean distances
        charges_norm_square = charges_norm**2
        mirror_charges_norm_square = mirror_charges_norm**2

        # calculate the potential matrix
        pot_matrix = C_EPS * np.log(mirror_charges_norm / charges_norm)

        # calculate the x- and y-components of the v matrix
        v_x = (
            charges_diff_x / charges_norm_square
            - mirror_charges_diff_x / mirror_charges_norm_square
        )
        v_y = (
            charges_diff_y / charges_norm_square
            - mirror_charges_diff_y / mirror_charges_norm_square
        )

        return pot_matrix, v_x, v_y

    def calc_ave_max_conductor_surface_gradient(self) -> bool:
        """Compute the average maximum surface gradient of the line bundles.

        This is required by the sound computation.

        This method will implicitly call the calc_conductor_surface_gradient and,
        thus, the user interface will only need to call this method if the
        average maximum surface gradient is to be recalculated before the
        audible noise calculations.

        The calculation will be saved as variables of the Line instances:

        * E_ac: average maximum surface gradient of the AC line [kV/cm]
        * E_dc: average maximum surface gradient of the DC line [kV/cm]

        The return value is a boolean status signaling the success of the
        calculation:

        * False: calculation aborted
        * True: calculation successful
        """

        # calculate the complete conductor surface gradient
        status = self.calc_conductor_surface_gradient()
        # abort calculation and return False if conducotr surface gradient
        # calculation cannot be performed
        if not status:
            return False

        try:
            # get the required surface gradient for the corresponding lines
            for sys_idx, system in enumerate(self.systems):
                for line_idx, line in enumerate(system.lines):
                    E_ac_max = []
                    E_dc_max = []
                    for con_idx, con in enumerate(line.cons):
                        # get the start and end indexes of the current line
                        if sys_idx == 0 and line_idx == 0 and con_idx == 0:
                            start = 0
                            end = len(con.contours)
                        else:
                            start = end + 1
                            end += len(con.contours)

                        # get the maximum surface gradients of conductors
                        # in a bundle (minimum for DC negative conductors)
                        E_ac_max.append(np.max(self.E_ac[start:end]))

                        max_val = np.max(self.E_dc[start:end])
                        min_val = np.min(self.E_dc[start:end])
                        if line.line_type == LineType.dc_pos:
                            E_dc_max.append(max_val)
                        elif line.line_type == LineType.dc_neg:
                            E_dc_max.append(min_val)
                        else:
                            E_dc_max.append(np.maximum(max_val, min_val))

                    # save the surface gradient in the correct unit [kV/cm]
                    line.E_ac = np.mean(E_ac_max) / 100000
                    line.E_dc = np.mean(E_dc_max) / 100000

                    # save the offset surface gradient (update: polarity independent)
                    line.E_ac_pos_offset = line.E_ac + np.abs(line.E_dc) / np.sqrt(2)
                    line.E_ac_neg_offset = line.E_ac_pos_offset

                    # include AC ripple (as rms) in DC surface gradient
                    line.E_dc_rip = np.abs(line.E_dc) + line.E_ac

        except AttributeError as e:
            print(e)

        # return True if calculation is successful
        return True

    def _check_line_collision(self) -> list[tuple[int, int]]:
        """Check for colissions between lines in the tower geometry configuration.

        If there is at least one line colission, the electric and
        magnetic field calculations cannot be done as this leads to an error
        in the Numpy matrix operation.

        The return value is a list containing tuples of colliding lines.
        """

        line_idx = []
        coords = []
        bundle_radii = []
        for system in self.systems:
            for line in system.lines:
                coords.append(np.array([line.line_x, line.line_y]))
                bundle_radii.append(line.bundle_radius)

        for i, coords_i in enumerate(coords):
            for j, coords_j in enumerate(coords):
                if i == j:
                    continue
                # calculate the difference between the distance between
                # lines and the sum of bundle radii
                dist = np.linalg.norm(coords_i - coords_j)
                sum_bundle_radii = bundle_radii[i] + bundle_radii[j]
                diff = dist - sum_bundle_radii
                # line colission exists if the difference is negative
                if diff < 0:
                    line_idx.append((i, j))

        return line_idx

    def save_tower_config(self, file_name: str) -> None:
        """Save the tower configuration as a JSON file in the specified path in file_name."""

        tow_param = []
        # add parameters belonging to the individual systems
        for system_idx, system in enumerate(self.systems):
            lines = [
                {
                    "line_type": line.line_type.name,
                    "line_x": line.line_x,
                    "line_y": line.line_y,
                    "con_radius": line.con_radius,
                    "num_con": line.num_con,
                    "bundle_radius": line.bundle_radius,
                    "con_angle_offset": line.con_angle_offset,
                }
                for line in system.lines
            ]

            tow_param.append(
                {
                    "system_idx": system_idx,
                    "system_type": system.system_type.name,
                    "voltage": system.voltage,
                    "current": system.current,
                    "lines": lines,
                }
            )

        try:
            # write the parameters into a text file
            with open(file_name, "w", encoding="utf-8") as f:
                json.dump(tow_param, f, indent=4)
        except PermissionError as e:
            print(e)

    def load_tower_config(self, file_name: str) -> None:
        """Load the tower geometry from a JSON file in the specified path given in file_name."""

        try:
            # load the tower configuration from a JSON file
            with open(file_name, encoding="utf-8") as f:
                tow_param = json.load(f)
        except PermissionError as e:
            print(e)
            return

        # Delete the current systems list and create a new list
        del self.systems[:]
        self.systems = []

        system_type_by_name = {t.name: t for t in SystemType}
        line_type_by_name = {t.name: t for t in LineType}

        for system_param in tow_param:
            system = System(
                system_type_by_name[system_param["system_type"]],
                system_param["voltage"],
                system_param["current"],
            )
            for line_param in system_param["lines"]:
                line = Line(
                    line_type_by_name[line_param["line_type"]],
                    line_param["line_x"],
                    line_param["line_y"],
                    line_param["con_radius"],
                    line_param["num_con"],
                    line_param["bundle_radius"],
                    line_param["con_angle_offset"],
                )
                system.add_line(line)
            self.add_system(system)
