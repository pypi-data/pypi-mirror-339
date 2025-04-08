"""Ui components for plots."""

import os
from collections.abc import Callable
from typing import Any

import matplotlib as mpl
import matplotlib.axes
import matplotlib.figure
import numpy as np
from kivy.core.window import Window
from kivy.logger import Logger
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy_garden.matplotlib.backend_kivy import FigureCanvasKivy, NavigationToolbar2Kivy
from matplotlib.collections import CircleCollection

from hvlbuzz import MODULE_DIR
from hvlbuzz.config.config import ColorConfig, Config, YAxis
from hvlbuzz.config.ini import ConfigLoader
from hvlbuzz.core import (
    ResultValues,
    compute_b_cross_section,
    compute_e_cross_section,
    compute_sound,
)
from hvlbuzz.physics.line import LineType
from hvlbuzz.physics.system import SystemType

from .gui_tools import move_tooltip, paint_blue, paint_white

mpl.use("module://kivy_garden.matplotlib.backend_kivy")


class ToolTip(Label):  # type: ignore[misc]
    """The implementation of ToolTip can be found in the buzz.kv file."""


class ToolbarButton(ButtonBehavior, Image):  # type: ignore[misc]
    """Instances of ToolbarButton are images which behave as a button.

    initialization variable(s):

    * text: the text to be shown on the button ToolTip
    """

    bind: Callable[[Any], Any]

    def __init__(self, text: str, **kwargs: Any) -> None:
        Window.bind(mouse_pos=self.on_mouse_pos)
        super().__init__(**kwargs)

        # initialize the ToolTip
        self.tooltip = ToolTip(text=text)

    def paint_bg_blue(self) -> None:
        """This method paints the button background blue."""
        paint_blue(self)

    def paint_bg_white(self) -> None:
        """This method paints the button background white."""
        paint_white(self)

    def on_mouse_pos(self, _win: Any, pos: tuple[float, float]) -> None:
        """This method shows and closes the tooltip depending on mouse position."""
        move_tooltip(self, pos=pos)

    def close_tooltip(self, *_args: Any) -> None:
        """This method removes the tooltip widget from the window."""
        Window.remove_widget(self.tooltip)

    def display_tooltip(self, *_args: Any) -> None:
        """This method adds the tooltip widget to the window."""
        Window.add_widget(self.tooltip)


class BuzzPlotToolbar(NavigationToolbar2Kivy):  # type: ignore[misc]
    """BuzzPlotToolbar adds Matplotlib figure utilities to the BuzzPlot instance.

    The available figure utilities are:

    * Home: switch to the first view
    * Backward: traverse to the last view
    * Forward: traverse to the next view
    * Pan: pan the plot
    * Zoom: zoom to the specified rectangle

    initialization variable(s):

    * canvas: the BuzzPlot canvas for which the toolbar should be created

    Each utility is bound to a ToolbarButton which exists in a BoxLayout.

    The pan and zoom utilities are toggle buttons. Once they are toggled on,
    they will stay active until the buttons are toggled off. The background of
    these buttons will stay blue as long as they are active. The pan button
    will be inactivated when the zoom button is toggled active and vice versa.
    """

    def __init__(self, canvas: FigureCanvasKivy, **_kwargs: Any) -> None:
        # set the size of the BoxLayout
        self.layout = BoxLayout(size_hint=(1, 0.1))
        super().__init__(canvas)

        # Get the path to the Matplotlib toolbar images
        image_dir = os.path.join(MODULE_DIR, "static", "images")

        def create_toolbutton(
            icon: str, text: str, on_press: Callable[[Any], None], on_release: Callable[[Any], None]
        ) -> ToolbarButton:
            btn_image = os.path.join(image_dir, icon)
            btn = ToolbarButton(source=btn_image, text=text)
            btn.bind(on_press=on_press)  # type: ignore[call-arg]
            btn.bind(on_release=on_release)  # type: ignore[call-arg]
            self.layout.add_widget(btn)
            return btn

        self.home_btn = create_toolbutton("home.png", "Home", self.home_press, self.home_release)
        self.back_btn = create_toolbutton("back.png", "Back", self.back_press, self.back_release)
        self.forward_btn = create_toolbutton(
            "forward.png", "Forward", self.forward_press, self.forward_release
        )
        self.zoom_btn = create_toolbutton(
            "zoom_to_rect.png", "Zoom", self.zoom_press, self.zoom_release
        )
        self.pan_btn = create_toolbutton("move.png", "Pan", self.pan_press, self.pan_release)
        # initializes the toggle status of the pan and zoom buttons
        self.pan_active = False
        self.zoom_active = False

    def home_press(self, _event: Any) -> None:
        """This method is prompted on the press of the home button."""
        self.home_btn.paint_bg_blue()

    def home_release(self, _event: Any) -> None:
        """This method is prompted on the release of the home button."""
        self.home_btn.paint_bg_white()
        self.home()

    def back_press(self, _event: Any) -> None:
        """This method is prompted on the press of the back button."""
        self.back_btn.paint_bg_blue()

    def back_release(self, _event: Any) -> None:
        """This method is prompted on the release of the back button."""
        self.back_btn.paint_bg_white()
        self.back()

    def forward_press(self, _event: Any) -> None:
        """This method is prompted on the press of the forward button."""
        self.forward_btn.paint_bg_blue()

    def forward_release(self, _event: Any) -> None:
        """This method is prompted on the release of the forward button."""
        self.forward_btn.paint_bg_white()
        self.forward()

    def pan_press(self, _event: Any) -> None:
        """This method is prompted on the press of the pan button."""
        if self.pan_active:
            self.pan_btn.paint_bg_white()
        else:
            self.pan_btn.paint_bg_blue()
            self.zoom_btn.paint_bg_white()
        self.pan_active = not self.pan_active

    def pan_release(self, _event: Any) -> None:
        """This method is prompted on the release of the pan button."""
        self.pan()

    def zoom_press(self, _event: Any) -> None:
        """This method is prompted on the press of the zoom button."""
        if self.zoom_active:
            self.zoom_btn.paint_bg_white()
        else:
            self.zoom_btn.paint_bg_blue()
            self.pan_btn.paint_bg_white()
        self.zoom_active = not self.zoom_active

    def zoom_release(self, _event: Any) -> None:
        """This method is prompted on the release of the zoom button."""
        self.zoom()


class BuzzPlot(BoxLayout):  # type: ignore[misc]
    """BoxLayout containing the Matplotlib plot and the corresponding BuzzPlotToolbar.

    The functions which are responsible for the
    plotting of tower geometries, audible noise level and annotating electric
    field strength is also contained in this class.

    initialization variable(s):

    * tower: is the instance of Tower class on which plotting operations
            are to be done. All calculations are contained within the Tower
            class definition. The BuzzPlot instance receives the numerical
            results and create the plot accordingly.

    The plotting settings, such as color and size, can be adjusted in the
    Kivy settings screen.
    """

    y_label: str = ""

    def __init__(self, result_values: ResultValues, cfg: ConfigLoader, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        # Change the BoxLayout orientation to vertical
        self.orientation = "vertical"
        self._fontsize = 12

        self.cfg = cfg

        # Create a Matplotlib figure canvas and its corresponding toolbar
        fig = mpl.figure.Figure()
        ax: Any = fig.add_axes((0.1, 0.1, 0.6, 0.8))
        self.fig = fig
        self.ax = ax
        self.distance_axis = ax.twinx()
        self.distance_axis.set_ylabel(
            "z [m]", size=self._fontsize, rotation=0, ha="right", va="bottom", labelpad=0
        )
        self.distance_axis.yaxis.set_label_coords(1.0, 1.01)
        self.fig_canvas = FigureCanvasKivy(fig)
        self.toolbar = BuzzPlotToolbar(self.fig_canvas)
        self.add_widget(self.fig_canvas)
        self.add_widget(self.toolbar.layout)

        self.result_values = result_values

    def _msg_line_collision(self, ax: mpl.axes.Axes) -> None:
        ax.text(
            0.5,
            0.5,
            "check for line collision",
            horizontalalignment="center",
            verticalalignment="center",
            transform=ax.transAxes,
        )

    def plot_tower_geometry(self) -> None:
        """This method plots the conductor midpoints as a scatter plot."""
        # clear primary axis
        self.distance_axis.clear()

        # create the scatter plots
        for system in self.result_values.tower.systems:
            for line in system.lines:
                # Get the colors of the scatter from the settings parser
                color = conductor_color(line.line_type, self.cfg.data.tower_geometry.color)
                radius_mult = self.cfg.data.tower_geometry.scatter_plot.radius_mult
                phi = 2.0 * np.pi / line.num_con * np.arange(line.num_con) + np.deg2rad(
                    line.con_angle_offset
                )
                line_pos = np.array([line.line_x, line.line_y])
                con_x, con_y = line_pos[:, None] + radius_mult * line.bundle_radius * np.array(
                    [np.cos(phi), np.sin(phi)]
                )
                self.distance_axis.scatter(con_x, con_y, color=color)

        # set the y-axis limits
        if not self.cfg.data.tower_geometry.scatter_plot.auto_axis:
            ymin = self.cfg.data.tower_geometry.scatter_plot.lower_axis
            ymax = self.cfg.data.tower_geometry.scatter_plot.upper_axis
            self.distance_axis.set_ylim(ymin, ymax)
        else:
            self.distance_axis.set_ylim(None, None)

        # adjust the legends and labels of the figure
        scatter_handles, scatter_labels = self.get_scatter_label()
        self.distance_axis.legend(
            scatter_handles,
            scatter_labels,
            bbox_to_anchor=(1.1, 1),
            loc=2,
            borderaxespad=0.0,
            fontsize=12,
        )

        # draw the changes to the plot
        self.fig_canvas.draw_idle()

    def get_scatter_label(self) -> tuple[list[CircleCollection], tuple[str, ...]]:
        """Generate the appropriate legends for the tower geometry scatter plot."""
        # create customs artists for the legend
        line_types, scatter_labels = zip(
            *[
                (LineType.ac_r, "AC"),
                (LineType.dc_pos, "DC Positive"),
                (LineType.dc_neg, "DC Negative"),
                (LineType.dc_neut, "DC Neutral"),
                (LineType.gnd, "Ground"),
            ]
        )
        size = [20]
        cfg_color = self.cfg.data.tower_geometry.color
        artists = [
            CircleCollection(size, facecolors=conductor_color(lt, cfg_color)) for lt in line_types
        ]
        return artists, scatter_labels

    def compute_values(self) -> None:
        """Compute the values needed for the plot."""
        msg = "Must be implemented in a derived class."
        raise NotImplementedError(msg)

    def plot_inner(self) -> None:
        """Plot the result values."""
        msg = "Must be implemented in a derived class."
        raise NotImplementedError(msg)

    def fetch_y_axis(self, config: Config) -> YAxis:
        """Fetch the appropriate y axis settings from the config."""
        msg = "Must be implemented in a derived class."
        raise NotImplementedError(msg)

    def plot(self) -> None:
        """Plot the data.

        The plot will overlap the tower geometry scatter plot but
        has its value shown on a secondary y-axis. The corresponding legend
        of the values will also be added.
        """
        # clear secondary axis
        self.ax.clear()
        try:
            self.compute_values()
        except RuntimeError as e:
            # print text if calculation is unsuccessful due to line collision
            self._msg_line_collision(self.ax)
            # draw changes to the plot
            self.fig_canvas.draw_idle()
            # log the error
            Logger.exception(format(e))
            return
        self.plot_inner()
        y_axis = self.fetch_y_axis(self.cfg.data)
        # set the y-axis limits
        if not y_axis.auto_axis:
            self.ax.set_ylim(ymin=y_axis.lower_axis, ymax=y_axis.upper_axis)
        else:
            self.ax.set_ylim(None, None)

        # adjust the legends and labels of the figure
        height = self.cfg.data.sound.ground_points.height_above_ground
        self.ax.legend(bbox_to_anchor=(1.1, 0), loc=3, borderaxespad=0.0, fontsize=self._fontsize)
        self.ax.set_xlabel("Lateral distance from line axis in m", size=self._fontsize)

        self.ax.set_ylabel(
            self.y_label.format(height),
            size=self._fontsize,
            rotation=0,
            ha="left",
            va="bottom",
            labelpad=0,
        )
        self.distance_axis.set_ylabel(
            "z [m]", size=self._fontsize, rotation=0, ha="right", va="bottom", labelpad=0
        )

        self.ax.yaxis.set_label_coords(0.0, 1.01)
        self.distance_axis.yaxis.set_label_coords(1.0, 1.01)
        self.ax.tick_params(axis="both", which="major", labelsize=self._fontsize)
        self.distance_axis.tick_params(axis="both", which="major", labelsize=self._fontsize)

        # draw the changes to the plot
        self.fig_canvas.draw_idle()

    def plot_clear(self) -> None:
        """Clear both axes of the figure."""
        # clear primary axis
        self.ax.clear()
        # clear secondary axis
        self.distance_axis.clear()
        # draw changes to the plot
        self.fig_canvas.draw_idle()


class BuzzPlotSound(BuzzPlot):
    """Specialization of BuzzPlot for sound levels."""

    y_label = "Sound level [dBA] at {} m over ground"

    def compute_values(self) -> None:
        """Compute the values needed for the plot."""
        self.result_values.sound = compute_sound(self.result_values.tower, self.cfg.data)

    def plot_inner(self) -> None:
        """Plot the result values."""
        values = self.result_values.sound
        x = values.x
        for L, plot in zip(values.L, values.plots):
            self.ax.plot(x, L, label=plot.name, color=plot.color, linewidth=4)

    def fetch_y_axis(self, config: Config) -> YAxis:
        """Fetch the appropriate y axis settings from the config."""
        return config.sound.y_axis


class BuzzPlotEField(BuzzPlot):
    """Specialization of BuzzPlot for the electric field."""

    y_label = "Electric field [kV/m] at {} m over ground"

    def compute_values(self) -> None:
        """Compute the values needed for the plot."""
        self.result_values.e_field = compute_e_cross_section(
            self.result_values.tower, self.cfg.data
        )

    def plot_inner(self) -> None:
        """Plot the result values."""
        tower = self.result_values.tower
        system_types = {system.system_type for system in tower.systems}

        if SystemType.ac in system_types:
            self.ax.plot(
                self.result_values.e_field.x,
                tower.E_ac_ground,
                label="AC E-Field",
                color="blue",
                linewidth=4,
            )
        if SystemType.dc in system_types or SystemType.dc_bipol in system_types:
            self.ax.plot(
                self.result_values.e_field.x,
                tower.E_dc_ground,
                label="DC E-Field",
                color="red",
                linewidth=4,
            )
        # log maximum electric field values
        Logger.info(
            "E-field plot: Height above ground = %s%s",
            str(self.result_values.e_field.h),
            "m",
        )
        Logger.info(
            "E-field plot: Max AC ground E-field = %s %s",
            str(np.max(tower.E_ac_ground)),
            "kV/m",
        )
        Logger.info(
            "E-field plot: Max DC ground E-field = %s %s",
            str(np.max(tower.E_dc_ground)),
            "kV/m",
        )

    def fetch_y_axis(self, config: Config) -> YAxis:
        """Fetch the appropriate y axis settings from the config."""
        return config.electric_field.y_axis


class BuzzPlotBField(BuzzPlot):
    """Specialization of BuzzPlot for the magnetic field."""

    y_label = "Magnetic field [\u03bcT] at {} m over ground"

    def compute_values(self) -> None:
        """Compute the values needed for the plot."""
        self.result_values.b_field = compute_b_cross_section(
            self.result_values.tower, self.cfg.data
        )

    def plot_inner(self) -> None:
        """Plot the result values."""
        tower = self.result_values.tower
        system_types = {system.system_type for system in tower.systems}

        if SystemType.ac in system_types:
            self.ax.plot(
                self.result_values.b_field.x,
                tower.B_ac,
                label="AC B-Field",
                color="blue",
                linewidth=4,
            )
        if SystemType.dc in system_types or SystemType.dc_bipol in system_types:
            self.ax.plot(
                self.result_values.b_field.x,
                tower.B_dc,
                label="DC B-Field",
                color="red",
                linewidth=4,
            )
        # log maximum magnetic field values
        Logger.info("B-field plot: Height above ground = %sm", str(self.result_values.b_field.h))
        Logger.info(
            "B-field plot: Max AC ground B-field = %s%s",
            str(np.max(tower.B_ac)),
            "e-6 T",
        )
        Logger.info(
            "B-field plot: Max DC ground B-field = %s%s",
            str(np.max(tower.B_dc)),
            "e-6 T",
        )

    def fetch_y_axis(self, config: Config) -> YAxis:
        """Fetch the appropriate y axis settings from the config."""
        return config.magnetic_field.y_axis


def conductor_color(line_type: LineType, config: ColorConfig) -> str:
    """Load the configured color for a given line type.

    Returns the first letter of the configured color.
    """
    color_by_line_type = {
        LineType.ac_r: config.ac_con_color,
        LineType.ac_s: config.ac_con_color,
        LineType.ac_t: config.ac_con_color,
        LineType.dc_pos: config.dc_pos_con_color,
        LineType.dc_neg: config.dc_neg_con_color,
        LineType.dc_neut: config.dc_neut_con_color,
        LineType.gnd: config.gnd_con_color,
    }
    color = color_by_line_type[line_type].value
    return "k" if color == "black" else color[0]
