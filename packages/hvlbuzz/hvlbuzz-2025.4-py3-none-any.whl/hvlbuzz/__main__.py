"""Entry point of the program."""

import sys
import traceback

from kivy import Config

from hvlbuzz.ui.main import BuzzApp

Config.set("graphics", "multisamples", "0")
Config.set("input", "mouse", "mouse,disable_multitouch")


def main() -> None:
    """Main routine."""
    try:
        BuzzApp().run()
    except Exception as e:  # noqa: BLE001
        print(f"An error occurred: {e}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
