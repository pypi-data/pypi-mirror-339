"""Ui component SystemAddPopup."""

from collections.abc import Callable
from typing import Any

import numpy as np
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.popup import Popup

from hvlbuzz.physics.line import Line, LineType
from hvlbuzz.physics.system import System, SystemType
from hvlbuzz.physics.tower import Tower
from hvlbuzz.ui.layout import DataTabbedPanel

from .system import SystemConfigBase
from .systemselector import SystemSelector


class SystemAddPopup(Popup, SystemConfigBase):  # type: ignore[misc]
    """Enables the users to add an new System instance to the tower configuration.

    initialization variable(s):

    * tower: Tower instance on which the new system is to be added
    * system_selector: SystemSelector instance used for system selection
    * data_tabbed_panel: DataTabbedPanel instance containing plots

    The layout of the SystemAddPopup class is defined in the buzz.kv file.
    """

    line_one_x = ObjectProperty(None)
    line_two_x = ObjectProperty(None)
    line_three_x = ObjectProperty(None)
    line_one_y = ObjectProperty(None)
    line_two_y = ObjectProperty(None)
    line_three_y = ObjectProperty(None)
    line_one_label = ObjectProperty(None)
    line_two_label = ObjectProperty(None)
    line_three_label = ObjectProperty(None)

    def __init__(
        self,
        tower: Tower,
        system_selector: SystemSelector,
        data_tabbed_panel: DataTabbedPanel,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)

        # Tower instance on which the new system is to be added
        self.tower = tower
        # SystemSelector instance used for system selection
        self.system_selector = system_selector
        # DataTabbedPanel instance containing plots
        self.data_tabbed_panel = data_tabbed_panel

        # setup the dropdown for system type selection
        self.setup_dropdown()

        # create a list containing all inputs for input checks
        self.param_input_list = [
            self.system_type,
            self.voltage,
            self.current,
            self.con_radius,
            self.num_con,
            self.bundle_radius,
            self.con_angle_offset,
            self.line_one_x,
            self.line_two_x,
            self.line_three_x,
            self.line_one_y,
            self.line_two_y,
            self.line_three_y,
        ]

    def setup_dropdown(self) -> None:
        """Sets up the dropdown for system type selection."""

        # create a DropDown instance
        self.dropdown = DropDown()
        # possible system types
        system_types = [
            ("AC", self.set_ac),
            ("DC Bipolar", self.set_dc_bipolar),
            ("DC with Neutral Line", self.set_dc_with_neutral_line),
            ("Ground Line", self.set_ground_line),
        ]

        def prepare_callback(
            text: str, inner_callback: Callable[[], None]
        ) -> Callable[[Any], None]:
            """This is needed to prevent cell-var-from-loop.

            https://pylint.pycqa.org/en/latest/user_guide/messages/warning/cell-var-from-loop.html.
            """

            def on_release(button: Any) -> None:
                self.dropdown.select(button.text)
                # change the text of the system type button
                self.system_type.text = text

                inner_callback()

            return on_release

        # add buttons to dropdown
        for sys_type, callback in system_types:
            btn = Button(text=sys_type, size_hint_y=None, height=44)
            btn.bind(on_release=prepare_callback(sys_type, callback))
            self.dropdown.add_widget(btn)
        # bind system_type button click to open dropdown
        self.system_type.bind(on_release=self.dropdown.open)

    def set_ac(self) -> None:
        """Set ac system type."""
        self.voltage.text = ""
        self.voltage.disabled = False
        self.current.text = ""
        self.current.disabled = False
        self.line_one_label.text = "AC R"
        self.line_two_label.text = "AC S"
        self.line_two_x.disabled = False
        self.line_two_x.opacity = 1
        self.line_two_y.disabled = False
        self.line_two_y.opacity = 1
        self.line_three_label.text = "AC T"
        self.line_three_x.disabled = False
        self.line_three_x.opacity = 1
        self.line_three_y.disabled = False
        self.line_three_y.opacity = 1

    def set_dc_bipolar(self) -> None:
        """Set dc bipolar system type."""
        self.voltage.text = ""
        self.voltage.disabled = False
        self.current.text = ""
        self.current.disabled = False
        self.line_one_label.text = "DC +"
        self.line_two_label.text = "DC -"
        self.line_two_x.disabled = False
        self.line_two_x.opacity = 1
        self.line_two_y.disabled = False
        self.line_two_y.opacity = 1
        self.line_three_label.text = ""
        self.line_three_x.disabled = True
        self.line_three_x.opacity = 0
        self.line_three_y.disabled = True
        self.line_three_y.opacity = 0

    def set_dc_with_neutral_line(self) -> None:
        """Set "dc with neutral" system type."""
        self.voltage.text = ""
        self.voltage.disabled = False
        self.current.text = ""
        self.current.disabled = False
        self.line_one_label.text = "DC +"
        self.line_two_label.text = "DC -"
        self.line_two_x.disabled = False
        self.line_two_x.opacity = 1
        self.line_two_y.disabled = False
        self.line_two_y.opacity = 1
        self.line_three_label.text = "DC Neutral"
        self.line_three_x.disabled = False
        self.line_three_x.opacity = 1
        self.line_three_y.disabled = False
        self.line_three_y.opacity = 1

    def set_ground_line(self) -> None:
        """Set "ground line" system type."""
        self.voltage.text = "0"
        self.voltage.disabled = True
        self.current.text = "0"
        self.current.disabled = True
        self.line_one_label.text = "Ground Line"
        self.line_two_label.text = ""
        self.line_two_x.disabled = True
        self.line_two_x.opacity = 0
        self.line_two_y.disabled = True
        self.line_two_y.opacity = 0
        self.line_three_label.text = ""
        self.line_three_x.disabled = True
        self.line_three_x.opacity = 0
        self.line_three_y.disabled = True
        self.line_three_y.opacity = 0

    def cancel(self) -> None:
        """This method is called when the Cancel button is pressed."""
        self.dismiss()
        self.input_clear()

    def input_check(self) -> bool:
        """This method checks whether inputs are empty."""
        empty_input_count = 0
        for number_input in self.param_input_list:
            if number_input.text == "" and not number_input.disabled:
                # change background to red if input is empty
                number_input.background_color = [1, 0, 0, 0.2]
                empty_input_count += 1
            else:
                # change background to white if input is not empty
                number_input.background_color = [1, 1, 1, 1]

        return empty_input_count <= 0

    def input_clear(self) -> None:
        """This method clears the inputs."""
        for number_input in self.param_input_list:
            number_input.text = ""
            number_input.background_color = [1, 1, 1, 1]

    def suggest_con_angle_offset(self, num_con: str) -> None:
        """Suggest the appropriate conductor angle offset depending on the number of conductors.

        The conductor angle offset
        will be updated immediately when the number of conductor is changed
        due to the method binding.
        """
        if num_con == "":
            self.con_angle_offset.text = ""
        elif num_con == "3":
            # the typical angle offset for 3 conductors is 30 degrees
            self.con_angle_offset.text = "30"
        elif num_con == "4":
            # the typical angle offset for 4 conductors is 45 degrees
            self.con_angle_offset.text = "45"
        else:
            self.con_angle_offset.text = "0"

    def add_system(self) -> None:
        """Adds a new system to the tower configuration.

        The units used for inputs by users are different from those used in
        the backend calculation. This method handles the unit conversion.
        """

        # check that input is not empty
        input_status = self.input_check()
        if not input_status:
            return

        # prepare the system type string
        system_type_by_text = {
            "AC": SystemType.ac,
            "DC with Neutral Line": SystemType.dc,
            "DC Bipolar": SystemType.dc_bipol,
            "Ground Line": SystemType.gnd,
        }
        system_type = system_type_by_text[self.system_type.text]

        # convert voltage from kV to V
        voltage = float(self.voltage.text) * 1000

        # convert current from kA to A
        current = float(self.current.text) * 1000

        num_con = int(self.num_con.text)

        # convert conductor diameter in mm to radius in m
        con_radius = float(self.con_radius.text) / 2000

        # convert bundle spacing in mm to bundle radius in m
        bundle_spacing = float(self.bundle_radius.text) / 1000
        bundle_radius = bundle_spacing / (2 * np.sin(np.pi / num_con))

        if num_con < 2 and bundle_radius != 0:
            bundle_radius = 0
        if num_con > 1 and bundle_radius == 0:
            num_con = 1

        con_angle_offset = float(self.con_angle_offset.text)

        # creates a new System instance with the inputs
        system = System(system_type, voltage, current)

        if not self.line_one_x.disabled and not self.line_one_y.disabled:
            line_type_by_system = {
                SystemType.ac: LineType.ac_r,
                SystemType.dc: LineType.dc_pos,
                SystemType.dc_bipol: LineType.dc_pos,
                SystemType.gnd: LineType.gnd,
            }
            line = Line(
                line_type=line_type_by_system[system_type],
                line_x=float(self.line_one_x.text),
                line_y=float(self.line_one_y.text),
                con_radius=con_radius,
                num_con=num_con,
                bundle_radius=bundle_radius,
                con_angle_offset=con_angle_offset,
            )
            system.add_line(line)

        if not self.line_two_x.disabled and not self.line_two_y.disabled:
            line_type_by_system = {
                SystemType.ac: LineType.ac_s,
                SystemType.dc: LineType.dc_neg,
                SystemType.dc_bipol: LineType.dc_neg,
            }
            line = Line(
                line_type=line_type_by_system[system_type],
                line_x=float(self.line_two_x.text),
                line_y=float(self.line_two_y.text),
                con_radius=con_radius,
                num_con=num_con,
                bundle_radius=bundle_radius,
                con_angle_offset=con_angle_offset,
            )
            system.add_line(line)

        if not self.line_three_x.disabled and not self.line_three_y.disabled:
            line_type_by_system = {SystemType.ac: LineType.ac_t, SystemType.dc: LineType.dc_neut}
            line = Line(
                line_type=line_type_by_system[system_type],
                line_x=float(self.line_three_x.text),
                line_y=float(self.line_three_y.text),
                con_radius=con_radius,
                num_con=num_con,
                bundle_radius=bundle_radius,
                con_angle_offset=con_angle_offset,
            )
            system.add_line(line)

        # adds the new System instannce to the tower systems array
        tower_status = self.tower.add_system(system)

        if not tower_status:
            # if tower_status is empty array, the addition was successful
            self.input_clear()
            self.system_selector.setup_system_select()
            self.data_tabbed_panel.update_plots()
            self.dismiss()
        else:
            line_by_index = {
                0: (self.line_one_x, self.line_one_y),
                1: (self.line_two_x, self.line_two_y),
                2: (self.line_three_x, self.line_three_y),
            }

            # if tower_status is a non-empty array, the addition failed

            # tower_status contains the line indexes 0, 1 or 2 which coincide
            # with other lines. Those lines will be marked red.
            for index in tower_status:
                line_x, line_y = line_by_index[index]
                line_x.background_color = [1, 0, 0, 0.2]
                line_y.background_color = [1, 0, 0, 0.2]
