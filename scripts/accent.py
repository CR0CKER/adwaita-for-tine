#!/usr/bin/env python3
"""Print the literal accent colours for theme.json from a GNOME accent.

Tine's theme packages only take literal colours, so the oklab lightness clamps
Adwaita for Logseq applies at runtime (themes/adwaita.css) are computed here:

    dark:  text max(L, 0.763), fill min(L, 0.674), hover max(L, 0.85)
    light: text min(L, 0.5),   fill max(L, 0.62),  hover min(L, 0.42)

Usage: scripts/accent.py [#rrggbb | blue | teal | green | yellow | orange | red |
pink | purple | slate]   (default: yellow)
"""
import math
import sys

# libadwaita's @accent_bg_color per GNOME accent name.
GNOME_ACCENTS = {
    "blue": "#3584e4", "teal": "#2190a4", "green": "#3a944a",
    "yellow": "#c88800", "orange": "#ed5b00", "red": "#e62d42",
    "pink": "#d56199", "purple": "#9141ac", "slate": "#6f8396",
}


def _to_linear(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _to_srgb(c):
    c = max(0.0, min(1.0, c))
    return 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055


def to_oklab(hex_colour):
    h = hex_colour.lstrip("#")
    r, g, b = (_to_linear(int(h[i:i + 2], 16) / 255) for i in (0, 2, 4))
    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    l, m, s = (math.copysign(abs(x) ** (1 / 3), x) for x in (l, m, s))
    return (0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s,
            1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s,
            0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s)


def from_oklab(L, a, b):
    l = (L + 0.3963377774 * a + 0.2158037573 * b) ** 3
    m = (L - 0.1055613458 * a - 0.0638541728 * b) ** 3
    s = (L - 0.0894841775 * a - 1.2914855480 * b) ** 3
    rgb = (4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
           -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
           -0.0041960863 * l - 0.7034186147 * m + 1.7076466463 * s)
    return "#" + "".join(f"{round(_to_srgb(c) * 255):02x}" for c in rgb)


def clamp(hex_colour, fn):
    L, a, b = to_oklab(hex_colour)
    return from_oklab(fn(L), a, b)


MODES = {
    "light": (lambda L: min(L, 0.5), lambda L: max(L, 0.62), lambda L: min(L, 0.42)),
    "dark": (lambda L: max(L, 0.763), lambda L: min(L, 0.674), lambda L: max(L, 0.85)),
}


def main():
    arg = sys.argv[1] if len(sys.argv) > 1 else "yellow"
    accent = GNOME_ACCENTS.get(arg, arg)
    for mode, (text, fill, hover) in MODES.items():
        fg = clamp(accent, text)
        bg = clamp(fg, fill)  # the fill derives from the clamped text colour
        r, g, b = (int(bg[i:i + 2], 16) for i in (1, 3, 5))
        print(f'"{mode}": {{')
        print(f'  "--ls-active-primary-color": "{bg}",')
        print(f'  "--ls-link-text-color": "{fg}",')
        print(f'  "--ls-link-text-hover-color": "{clamp(fg, hover)}",')
        print(f'  "--ls-tag-text-color": "{fg}",')
        print(f'  "--ls-selection-background-color": "rgba({r}, {g}, {b}, 0.3)"')
        print("}")


if __name__ == "__main__":
    main()
