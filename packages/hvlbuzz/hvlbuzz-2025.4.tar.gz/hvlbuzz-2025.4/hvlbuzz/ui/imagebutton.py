"""ImageButton ui component."""

from typing import Any

from kivy.core.window import Window
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.label import Label

from .gui_tools import move_tooltip, paint_blue, paint_white


class ToolTip(Label):  # type: ignore[misc]
    """The implementation of ToolTip can be found in the buzz.kv file."""


class ImageButton(ButtonBehavior, Image):  # type: ignore[misc]
    """Instances of ImageButton are images which behave as a button.

    initialization variable(s):

    * img: path to the image to be used on the button
    * text: the text to be shown on the button ToolTip
    """

    def __init__(self, img: str, text: str, **kwargs: Any) -> None:
        Window.bind(mouse_pos=self.on_mouse_pos)
        super().__init__(**kwargs)

        # initialize the image
        self.source = img
        # initialize the ToolTip
        self.tooltip = ToolTip(text=text)

    def on_press(self) -> None:
        """This method paints the background blue on button press."""
        paint_blue(self)

    def on_release(self) -> None:
        """This method paints the background white on button release."""
        paint_white(self)

    def on_mouse_pos(self, _win: Any, pos: tuple[float, float]) -> None:
        """This method shows and closes the tooltip depending on mouse position."""
        move_tooltip(self, pos=pos, shift_x=-self.tooltip.width)

    def close_tooltip(self, *_args: Any) -> None:
        """This method removes the tooltip widget from the window."""
        Window.remove_widget(self.tooltip)

    def display_tooltip(self, *_args: Any) -> None:
        """This method adds the tooltip widget to the window."""
        Window.add_widget(self.tooltip)
