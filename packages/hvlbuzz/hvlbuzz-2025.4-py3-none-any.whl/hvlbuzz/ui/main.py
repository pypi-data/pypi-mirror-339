"""Main UI application."""

from __future__ import annotations

import os
import sys
from typing import TYPE_CHECKING, Any, ClassVar

from kivy.app import App
from kivy.logger import Logger
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.settings import Settings, SettingsWithSidebar

from hvlbuzz import MODULE_DIR, __version__
from hvlbuzz.config.config import Config as MainConfig
from hvlbuzz.config.ini import buzz_ini_path
from hvlbuzz.export.csv import export_csv
from hvlbuzz.export.pdf import export_pdf
from hvlbuzz.physics.tower import Tower
from hvlbuzz.ui.config.layout import ConfigLayout
from hvlbuzz.ui.config.systemaddpopup import SystemAddPopup
from hvlbuzz.ui.config.systemselector import SystemSelector
from hvlbuzz.ui.config.toolbar import ConfigToolbar
from hvlbuzz.ui.dataclass_settings_panel import set_defaults, settings_add_dataclass_panels
from hvlbuzz.ui.layout import DataTabbedPanel
from hvlbuzz.ui.numeric_input import FloatInput, IntegerInput

if os.name == "nt":
    import win32api

if TYPE_CHECKING:
    from kivy import Config

# Need to be in globals for buzz.kv, otherwise unused import:
_custom_widgets = (FloatInput, IntegerInput)


class BuzzNewDialog(FloatLayout):  # type: ignore[misc]
    """Layout on a popup which allows users to clear the current tower geometry."""

    clear_tower = ObjectProperty(None)
    cancel = ObjectProperty(None)


class BuzzLoadDialog(FloatLayout):  # type: ignore[misc]
    """Layout on a popup which allows users to load the tower geometry from a JSON file."""

    load = ObjectProperty(None)
    cancel = ObjectProperty(None)
    load_filechooser = ObjectProperty(None)
    text_input = ObjectProperty(None)
    drive_spinner = ObjectProperty(None)

    def __init__(self, load_path: str, **kwargs: Any):
        super().__init__(**kwargs)

        # set the current working directory as starting path of filechooser
        if os.path.isdir(load_path):
            self.load_filechooser.path = load_path
            self.text_input.text = load_path
        else:
            self.load_filechooser.path = os.getcwd()
            self.text_input.text = os.getcwd()

        if os.name == "nt":
            drives = win32api.GetLogicalDriveStrings()
            self.drive_spinner.values = drives.split("\000")[:-1]

        else:
            self.drive_spinner.values = []


class BuzzSaveDialog(FloatLayout):  # type: ignore[misc]
    """Layout on a popup which allows users to save the current tower geometry as a JSON file."""

    save = ObjectProperty(None)
    cancel = ObjectProperty(None)
    save_filechooser = ObjectProperty(None)
    text_input = ObjectProperty(None)
    text_input_dir = ObjectProperty(None)
    drive_spinner = ObjectProperty(None)

    def __init__(self, save_path: str, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        # set the current working directory as starting path of filechooser
        if os.path.isdir(save_path):
            self.save_filechooser.path = save_path
            self.text_input_dir.text = save_path
        else:
            self.save_filechooser.path = os.getcwd()
            self.text_input_dir.text = os.getcwd()

        if os.name == "nt":
            drives = win32api.GetLogicalDriveStrings()
            self.drive_spinner.values = drives.split("\000")[:-1]

        else:
            self.drive_spinner.values = []


class ExportCSVDialog(FloatLayout):  # type: ignore[misc]
    """Layout on a popup which allows users to save the plot and table data in a CSV file."""

    export_csv = ObjectProperty(None)
    cancel = ObjectProperty(None)
    export_csv_filechooser = ObjectProperty(None)
    text_input = ObjectProperty(None)
    text_input_dir = ObjectProperty(None)
    drive_spinner = ObjectProperty(None)

    def __init__(self, export_path: str, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        # set the current working directory as starting path of filechooser
        if os.path.isdir(export_path):
            self.export_csv_filechooser.path = export_path
            self.text_input_dir.text = export_path
        else:
            self.export_csv_filechooser.path = os.getcwd()
            self.text_input_dir.text = os.getcwd()

        if os.name == "nt":
            drives = win32api.GetLogicalDriveStrings()
            self.drive_spinner.values = drives.split("\000")[:-1]

        else:
            self.drive_spinner.values = []


class ExportPDFDialog(FloatLayout):  # type: ignore[misc]
    """Layout on a popup which allows users to save the plots and tables in a PDF file."""

    export_pdf = ObjectProperty(None)
    cancel = ObjectProperty(None)
    export_pdf_filechooser = ObjectProperty(None)
    text_input = ObjectProperty(None)
    text_input_dir = ObjectProperty(None)
    drive_spinner = ObjectProperty(None)

    def __init__(self, export_path: str, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        # set the current working directory as starting path of filechooser
        if os.path.isdir(export_path):
            self.export_pdf_filechooser.path = export_path
            self.text_input_dir.text = export_path
        else:
            self.export_pdf_filechooser.path = os.getcwd()
            self.text_input_dir.text = os.getcwd()

        if os.name == "nt":
            drives = win32api.GetLogicalDriveStrings()
            self.drive_spinner.values = drives.split("\000")[:-1]

        else:
            self.drive_spinner.values = []


class ExportPNGDialog(FloatLayout):  # type: ignore[misc]
    """Layout on a popup which allows users to save a specific plot as a PNG image file."""

    export_png = ObjectProperty(None)
    cancel = ObjectProperty(None)
    dropdown_button = ObjectProperty(None)
    export_png_filechooser = ObjectProperty(None)
    text_input = ObjectProperty(None)
    text_input_dir = ObjectProperty(None)
    drive_spinner = ObjectProperty(None)

    options = ("Audible Noise", "Electric Field", "Magnetic Field")

    def __init__(self, export_path: str, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        # set the current working directory as starting path of filechooser
        if os.path.isdir(export_path):
            self.export_png_filechooser.path = export_path
            self.text_input_dir.text = export_path
        else:
            self.export_png_filechooser.path = os.getcwd()
            self.text_input_dir.text = os.getcwd()

        if os.name == "nt":
            drives = win32api.GetLogicalDriveStrings()
            self.drive_spinner.values = drives.split("\000")[:-1]
        else:
            self.drive_spinner.values = []

        # create a dropdown for the plot options
        self.plot_dropdown = DropDown()
        self.setup_dropdown()

    def setup_dropdown(self) -> None:
        """Sets up the dropdown and handles the method bindings."""
        for option in self.options:
            btn = Button(text=option, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: self.plot_dropdown.select(btn.text))
            self.plot_dropdown.add_widget(btn)
        self.dropdown_button.bind(on_release=self.plot_dropdown.open)
        self.plot_dropdown.bind(on_select=lambda _instance, x: self.set_option(x))

    def set_option(self, option: str) -> None:
        """Change the dropdown button text when a dropdown option is chosen."""
        self.dropdown_button.text = option + " \u25bc"


class HelpDoc(FloatLayout):  # type: ignore[misc]
    """Layout on a popup which shows the users the help documentation as an RST document."""

    rst_doc = ObjectProperty(None)
    close = ObjectProperty(None)

    doc_sources: ClassVar[dict[str, str]] = {
        "E-field CSM": os.path.join(MODULE_DIR, "static", "helpdocs", "help.rst"),
    }

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.rst_doc.source = os.path.join(MODULE_DIR, "static", "helpdocs", "help.rst")


class MainLayout(BoxLayout):  # type: ignore[misc]
    """Foundation layout of the application composing different sublayouts.

    MainLayout also handles the functionalities of the popup classes.
    """

    data_tabbed_panel = ObjectProperty(None)
    config_layout = ObjectProperty(None)
    selector_and_toolbar = ObjectProperty(None)

    _loaded_json: str | None = None

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        # Tower instance on which all methods work on
        self.tower = Tower()

        # add the DataTabbedPanel widget
        self.dtp = DataTabbedPanel(self.tower)
        self.data_tabbed_panel.add_widget(self.dtp)

        # add the ConfigLayout widget
        self.cl = ConfigLayout(self.tower)
        self.config_layout.add_widget(self.cl)

        # create a SystemSelector instance
        self.ss = SystemSelector(self.tower, self.cl)
        self.selector_and_toolbar.add_widget(self.ss)

        # create a SystemAddPopup instance
        self.sap = SystemAddPopup(self.tower, self.ss, self.dtp)

        # add the ConfigToolbar widget
        self.ct = ConfigToolbar(self.tower, self.dtp, self.sap, self.cl, self.ss)
        self.selector_and_toolbar.add_widget(self.ct)

        self._popup: Popup | None = None

    def show_new(self) -> None:
        """Shows the BuzzNewDialog popup."""
        content = BuzzNewDialog(clear_tower=self.clear_tower, cancel=self.dismiss_popup)
        self._popup = Popup(title="New Tower Configuration", content=content, size_hint=(0.9, 0.3))
        self._popup.open()

    def clear_tower(self) -> None:
        """Clears the tower configuration and resets all layouts."""
        self.tower.reset_systems()
        self.ss.setup_system_select()
        self.cl.remove_active_system()
        self.dtp.update_plots()
        self.dismiss_popup()

    def show_export_csv(self) -> None:
        """Shows the ExportCSVDialog popup."""
        content = ExportCSVDialog(
            export_path=self.dtp.cfg.data.export.csv_path,
            export_csv=self.export_csv,
            cancel=self.dismiss_popup,
        )
        self._popup = Popup(title="Export CSV", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def export_csv(self, path: str, filename: str) -> None:
        """Saves the plot and table data into a CSV file.

        input variable(s):

        * path: the directory path to save the CSV file in
        * filename: the name of the CSV file
        """
        # do not do anything if filename is still empty
        if filename == "":
            return

        config = App.get_running_app().config
        config.set("Export", "csv_path", os.path.dirname(os.path.join(path, filename)))
        config.write()

        try:
            export_csv(
                os.path.join(path, filename),
                self.dtp.result_values,
                self.dtp.cfg.data,
                self._loadedJSON,
            )
        except PermissionError:
            file_path = os.path.join(path, filename)
            Logger.exception("Export CSV: Permission denied to: %s", file_path)
        self.dismiss_popup()

    def show_export_pdf(self) -> None:
        """Shows the ExportPDFDialog popup."""
        content = ExportPDFDialog(
            export_path=self.dtp.cfg.data.export.pdf_path,
            export_pdf=self.export_pdf,
            cancel=self.dismiss_popup,
        )
        self._popup = Popup(title="Export PDF", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def export_pdf(self, path: str, filename: str) -> None:
        """Creates a PDF file with current plots and table.

        input variable(s):

        * path: the directory path to save the PDF file in
        * filename: the filename of the PDF file
        """
        # do not do anything if filename is still empty
        if filename == "":
            return

        full_path = os.path.join(path, filename)
        config = App.get_running_app().config
        config.set("Export", "pdf_path", os.path.dirname(full_path))
        config.write()
        try:
            export_pdf(
                full_path,
                result_values=self.dtp.result_values,
                config=self.dtp.cfg.data,
                loaded_json=self._loadedJSON,
                sound_fig=self.dtp.audible_noise_plot.buzz_plot.fig,
                e_fig=self.dtp.electric_field_plot.buzz_plot.fig,
                b_fig=self.dtp.magnetic_field_plot.buzz_plot.fig,
            )

        except PermissionError as e:
            print(e, file=sys.stderr)

        self.dismiss_popup()

    def show_helpdoc(self) -> None:
        """Shows the HelpDoc popup."""
        content = HelpDoc(close=self.dismiss_popup)
        self._popup = Popup(title="Help", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def show_aboutbox(self) -> None:
        """Shows the about box popup."""
        content = Label(
            text=f"""Version {__version__}

Originally, HVLBuzz was developed by Aldo Tobler under the supervision of
Christian M. Franck, Sören Hedtke and support by Mikołaj Rybiński at
ETH Zurich's High Voltage Laboratory.

Currently, it is maintained by FKH Zürich.

Further Information at https://gitlab.com/ethz_hvl/hvlbuzz and
https://hvl.ee.ethz.ch/publications-and-awards/Software.html


Press ESC to dismiss"""
        )
        self._popup = Popup(title="About HVLBuzz", content=content)
        self._popup.open()

    def show_export_png(self) -> None:
        """Shows the ExportPNGDialog popup."""
        content = ExportPNGDialog(
            export_path=self.dtp.cfg.data.export.png_path,
            export_png=self.export_png,
            cancel=self.dismiss_popup,
        )
        self._popup = Popup(title="Export PNG", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def export_png(self, path: str, filename: str, option: str) -> None:
        """Saves the chosen plot as a PNG image file.

        input variable(s):

        * path: the directory path to save the PNG image file in
        * filename: the name of the PNG image file
        * option: the plot chosen to be saved
        """
        # do not do anything if filename is still empty
        if filename == "":
            return

        config = App.get_running_app().config
        config.set("Export", "png_path", os.path.dirname(os.path.join(path, filename)))
        config.write()
        option = option[:-2]
        if option == "Audible Noise":
            fig = self.dtp.audible_noise_plot.buzz_plot.fig
        elif option == "Electric Field":
            fig = self.dtp.electric_field_plot.buzz_plot.fig
        elif option == "Magnetic Field":
            fig = self.dtp.magnetic_field_plot.buzz_plot.fig
        else:
            return
        if ".png" not in filename:
            filename += ".png"
        try:
            path = os.path.join(path, filename)
            # set the size of the image for better quality
            fig.set_size_inches(7, 7)
            fig.savefig(path)
        except PermissionError as e:
            print(e, file=sys.stderr)
        self.dismiss_popup()

    def show_load(self) -> None:
        """Shows the BuzzLoadDialog popup."""
        content = BuzzLoadDialog(
            load=self.load, cancel=self.dismiss_popup, load_path=self.dtp.cfg.data.export.load_path
        )
        self._popup = Popup(
            title="Load a Tower Configuration JSON File",
            content=content,
            size_hint=(0.9, 0.9),
        )
        self._popup.open()

    def load(self, path: str, selection: list[str]) -> None:
        """Handles the loading of the tower configuration from a JSON file.

        input variable(s):

        * path: the directory path where the JSON file is to be found
        * selection: the filenames selected
        """
        if len(selection) > 0 or path.endswith(".json"):
            if path.endswith(".json"):
                selection = [os.path.basename(path)]
                path = os.path.dirname(path)
            try:
                config = App.get_running_app().config
                config.set(
                    "Export",
                    "load_path",
                    os.path.dirname(os.path.join(path, selection[0])),
                )
                config.write()
                self._loadedJSON = os.path.basename(os.path.join(path, selection[0]))

                load_file = os.path.join(path, selection[0])
                self.tower.load_tower_config(load_file)
            except KeyError:
                Logger.exception("Buzz Error: cannot open %s", load_file)
                self.dismiss_popup()
                return
            self.ss.setup_system_select()
            self.cl.remove_active_system()
            self.dtp.update_plots()
            self.dismiss_popup()

    def show_save(self) -> None:
        """Shows the BuzzSaveDialog popup."""
        content = BuzzSaveDialog(
            save=self.save, cancel=self.dismiss_popup, save_path=self.dtp.cfg.data.export.save_path
        )
        self._popup = Popup(
            title="Save the Current Tower Configuration as a JSON File",
            content=content,
            size_hint=(0.9, 0.9),
        )
        self._popup.open()

    def save(self, path: str, filename: str) -> None:
        """Handles the saving of the tower configuration to a JSON file.

        input variable(s):

        * path: the directory path where the JSON file is to be found
        * selection: the filenames selected
        """
        self.cl.set_params()
        if len(filename) > 0:
            config = App.get_running_app().config
            config.set("Export", "save_path", os.path.dirname(os.path.join(path, filename)))
            config.write()
            self.tower.save_tower_config(os.path.join(path, filename + ".json"))
            self.dismiss_popup()

    def dismiss_popup(self) -> None:
        """Closes the active popup."""
        if self._popup is not None:
            self._popup.dismiss()


class BuzzApp(App):  # type: ignore[misc]
    """Main application.

    BuzzApp handles the settings and returns MainLayout as the user interface.
    """

    kv_directory = os.path.join(MODULE_DIR, "static")

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.main_layout: MainLayout | None = None
        # change the icon from default Kivy logo
        self.icon = os.path.join(MODULE_DIR, "static", "images", "buzz_logo.png")
        # define the style of the settings
        self.settings_cls = SettingsWithSidebar

    def get_application_config(self, _defaultpath: str = "%(appdir)s/%(appname)s.ini") -> str:
        """Override kivy's default config path."""
        return buzz_ini_path()

    def build(self) -> MainLayout:
        """Build the main layout."""
        self.main_layout = MainLayout()
        return self.main_layout

    def build_config(self, config: Config) -> None:
        """Sets up the settings page."""

        # define the default values for config
        set_defaults(MainConfig, config)

    def build_settings(self, settings: Settings) -> None:
        """Load the settings layout from the corresponding JSON files."""
        settings_add_dataclass_panels(settings, MainConfig, self.config)

    def on_config_change(self, _config: Any, _section: Any, _key: Any, _value: Any) -> None:
        """Reload config from buzz.ini."""
        if self.main_layout is not None:
            self.main_layout.dtp.cfg.update()
