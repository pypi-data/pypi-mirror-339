"""String representations for line types."""

from hvlbuzz.physics.line import LineType

LINE_TYPES = {
    LineType.ac_r: "AC R",
    LineType.ac_s: "AC S",
    LineType.ac_t: "AC T",
    LineType.dc_pos: "DC +",
    LineType.dc_neg: "DC -",
    LineType.dc_neut: "DC Neutral",
    LineType.gnd: "GND",
}
