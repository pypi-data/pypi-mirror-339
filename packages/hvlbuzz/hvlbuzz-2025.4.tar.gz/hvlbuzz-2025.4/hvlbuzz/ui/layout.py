"""Several ui layout components."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.tabbedpanel import TabbedPanel

from hvlbuzz.config.ini import ConfigLoader
from hvlbuzz.core import ResultValues
from hvlbuzz.export.csv import BASE_HEADER, table_header, tabularize

from .plot import (
    BuzzPlot,
    BuzzPlotBField,
    BuzzPlotEField,
    BuzzPlotSound,
)

if TYPE_CHECKING:
    from hvlbuzz.physics.tower import Tower


class TableHeaderLabel(Label):  # type: ignore[misc]
    """Special Label with border that is used in the TableLayout instance for the table headers.

    The implementation of this class can be found in the buzz.kv file.
    """


class TableContentLabel(Label):  # type: ignore[misc]
    """Special Label with border that is used in the TableLayout instance for the table contents.

    The implementation of this class can be found in the buzz.kv file.
    """


class TableLayout(GridLayout):  # type: ignore[misc]
    """Contains the electric field and sound level information complementing the sound plot.

    The information shown on the table is:

    * line type
    * line coordinates [m]
    * average maximum AC bundle electric field [kV/cm]
    * average maximum DC bundle electric field [kV/cm]
    * audible noise power level [W/m]

    initialization variable(s):

    * tower: Tower instance which holds the electric field and audible noise
            information

    The table is created with the RecycleView class from the Kivy module. The
    implementation of the layout can be found in the buzz.kv file.
    """

    def __init__(self, tower: Tower, cfg: ConfigLoader, L_names: list[str], **kwargs: Any) -> None:
        super().__init__(cols=len(BASE_HEADER) + len(L_names), **kwargs)
        # Tower instance which holds the electric field and audible noise info
        self.tower = tower
        self.cfg = cfg
        self.header_widgets: list[TableHeaderLabel] = []
        self.table_structure(L_names)

    def table_structure(self, L_names: list[str]) -> None:
        """Setup the structure of the table."""

        # initialize the table headers
        self.headers = table_header(L_names, self.cfg.data.sound.general_settings.an_unit)
        self.cols = len(self.headers)
        for w in self.header_widgets:
            self.remove_widget(w)
        self.header_widgets = [TableHeaderLabel(text=header) for header in self.headers]
        for w in self.header_widgets:
            self.add_widget(w)

    def update_table(self, result_values: ResultValues) -> None:
        """This method updates the table entry after recalculation."""

        # clear the GridLayout
        self.clear_widgets()

        # update the RecycleView data
        self.table_structure(result_values.sound.L_names())
        entries = [val for row in tabularize(result_values) for val in row]
        for entry in entries:
            self.add_widget(TableContentLabel(text=entry))


class PlotLayout(BoxLayout):  # type: ignore[misc]
    """Contains a BuzzPlot instance used to present the sound / field and tower geometry plots.

    :param result_values: Values and tower configuration to plot
    :param plot_callback: The callback used to plot
    """

    def __init__(
        self,
        result_values: ResultValues,
        plot: BuzzPlot,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)

        # create a BuzzPlot instance and adds it to the layout
        self.buzz_plot = plot
        self.tower = result_values.tower
        self.add_widget(self.buzz_plot)

    def plot(self) -> None:
        """Prompt the BuzzPlot instance to refresh plots.

        This includes the tower geometry and sound plots if there are one or more systems in
        the tower instance or clear the plots else.
        """
        if len(self.tower.systems) > 0:
            self.buzz_plot.plot_tower_geometry()
            self.buzz_plot.plot()
        else:
            self.buzz_plot.plot_clear()


class DataTabbedPanel(TabbedPanel):  # type: ignore[misc]
    """Inherits from the Kivy TabbedPanel class.

    Contains the TableLayout, AudibleNoisePlotLayout, ElectricFieldPlotLayout and
    MagneticFieldPlotLayout instances and present them in different tabs. Users
    can select which plots or table they are willing to see by clicking on the
    tabs. The active tab is shown with a blue bottom border.

    initialization variable(s):

    * tower: Tower instance which calculates the plot data

    The implementation of the layout can be found in the buzz.kv file.
    """

    audible_noise = ObjectProperty(None)
    table = ObjectProperty(None)
    electric_field = ObjectProperty(None)
    magnetic_field = ObjectProperty(None)

    def __init__(self, tower: Tower, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.cfg = ConfigLoader()

        # Collected numerical result values and tower configuration
        self.result_values = ResultValues(tower)

        self.audible_noise_plot = PlotLayout(
            self.result_values, BuzzPlotSound(self.result_values, self.cfg)
        )
        self.audible_noise.add_widget(self.audible_noise_plot)

        self.table_layout = TableLayout(
            self.result_values.tower, self.cfg, self.result_values.sound.L_names()
        )
        self.table.add_widget(self.table_layout)

        self.electric_field_plot = PlotLayout(
            self.result_values, BuzzPlotEField(self.result_values, self.cfg)
        )
        self.electric_field.add_widget(self.electric_field_plot)

        self.magnetic_field_plot = PlotLayout(
            self.result_values, BuzzPlotBField(self.result_values, self.cfg)
        )
        self.magnetic_field.add_widget(self.magnetic_field_plot)

        self.table_layout_x: TableLayout | None = None

    def update_plots(self) -> None:
        """This method prompts the update of all plots and table."""
        self.audible_noise_plot.plot()
        self.electric_field_plot.plot()
        self.magnetic_field_plot.plot()
        self.table_layout.update_table(self.result_values)
