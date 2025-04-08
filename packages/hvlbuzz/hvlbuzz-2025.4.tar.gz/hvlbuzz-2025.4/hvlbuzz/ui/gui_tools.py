"""Shared ui helper functions."""

import kivy.uix.widget
from kivy.clock import Clock
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Rectangle


def move_tooltip(
    widget: kivy.uix.widget.Widget, pos: tuple[float, float], shift_x: float = 0.0
) -> None:
    """Shows and closes the tooltip depending on mouse position."""
    if not widget.get_root_window():
        return
    # set the tooltip position
    widget.tooltip.pos = (pos[0] + shift_x, pos[1])
    # cancel scheduled event if cursor is moved
    Clock.unschedule(widget.display_tooltip)
    # close if cursor is opened
    widget.close_tooltip()
    if widget.collide_point(*widget.to_widget(*pos)):
        Clock.schedule_once(widget.display_tooltip, 1)


def paint_blue(widget: kivy.uix.widget.Widget) -> None:
    """Paints the background of a widget blue."""
    with widget.canvas.before:
        Color(0.1961, 0.6431, 0.8078, 1)
        Rectangle(size=widget.size, pos=widget.pos)


def paint_white(widget: kivy.uix.widget.Widget) -> None:
    """Paints the background of a widget white."""
    with widget.canvas.before:
        Color(1.0, 1.0, 1.0, 1.0)
        Rectangle(size=widget.size, pos=widget.pos)
