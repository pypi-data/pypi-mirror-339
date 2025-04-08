"""Entry point of the program when using pyinstaller."""

import os

# disable logging before loading kivy, otherwise the packaged version will crash
os.environ["KIVY_NO_CONSOLELOG"] = "1"

import kivy.resources
from kivy import Config

Config.set("graphics", "multisamples", "0")
Config.set("input", "mouse", "mouse,disable_multitouch")

if __name__ == "__main__":
    kivy.resources.resource_add_path(os.path.dirname(__file__))
    from hvlbuzz.__main__ import main

    main()
