"""Color related operations"""

import colorsys

from colorsys import (
    rgb_to_hls,
    hls_to_rgb,
    rgb_to_hsv,
    hsv_to_rgb,
    rgb_to_yiq,
    yiq_to_rgb,
)

from random import random
from dataclasses import dataclass
from typing import Sequence

from ..graphics.common import common_properties, Point
from ..graphics.all_enums import ColorSpace, Types


def change_hue(color: 'Color', delta: float) -> 'Color':
    """Changes the hue of a color by a specified delta value.

    Args:
        color: The Color object to modify.
        delta: The amount to adjust the hue value (between 0.0 and 1.0).
            Positive values increase hue, negative values decrease it.

    Returns:
        A new Color instance with the modified hue value.
    """
    r, g, b, a = color.rgba
    hls = colorsys.rgb_to_hls(r, g, b)
    r, g, b = colorsys.hls_to_rgb(hls[0] + delta, hls[1], hls[2])
    return Color(r, g, b, a)


def change_lightness(color: 'Color', delta: float) -> 'Color':
    """Changes the lightness of a color by a specified delta value.

    Args:
        color: The Color object to modify.
        delta: The amount to adjust the lightness value (between -1.0 and 1.0).
            Positive values increase lightness, negative values decrease it.

    Returns:
        A new Color instance with the modified lightness value.
    """
    r, g, b, a = color.rgba
    hls = colorsys.rgb_to_hls(r, g, b)
    r, g, b = colorsys.hls_to_rgb(hls[0], hls[1] + delta, hls[2])
    return Color(r, g, b, a)


def change_saturation(color: 'Color', delta: float) -> 'Color':
    """Changes the saturation of a color by a specified delta value.

    Args:
        color: The Color object to modify.
        delta: The amount to adjust the saturation value (between -1.0 and 1.0).
            Positive values increase saturation, negative values decrease it.

    Returns:
        A new Color instance with the modified saturation value.
    """
    r, g, b, a = color.rgba
    hls = colorsys.rgb_to_hls(r, g, b)
    r, g, b = colorsys.hls_to_rgb(hls[0], hls[1], hls[2] + delta)
    return Color(r, g, b, a)


def change_alpha(color, delta):
    r, g, b, a = color.rgba
    return Color(r, g, b, a + delta)


def change_red(color, delta):
    r, g, b, a = color.rgba
    return Color(r + delta, g, b, a)


def change_green(color, delta):
    r, g, b, a = color.rgba
    return Color(r, g + delta, b, a)


def change_blue(color, delta):
    r, g, b, a = color.rgba
    return Color(r, g, b + delta, a)


def rgb255to1(rgb):
    return [x / 255 for x in rgb]


def rgb1to255(rgb):
    return [int(x * 255) for x in rgb]


def hex_to_rgb(hexa):
    """Convert hex to RGB."""
    return tuple([int(hexa[i : i + 2], 16) for i in [0, 2, 4]])


def rgb_to_hex(r, g, b):
    """Convert RGB to hex."""
    return f"{r:X}{g:X}{b:X}"


@dataclass
class Color:
    """A class representing an RGB or RGBA color.

    This class represents a color in RGB or RGBA color space. The default values
    for the components are normalized between 0.0 and 1.0. Values outside this range
    are automatically converted from the 0-255 range.

    Attributes:
        red: The red component of the color (0.0 to 1.0).
        green: The green component of the color (0.0 to 1.0).
        blue: The blue component of the color (0.0 to 1.0).
        alpha: The alpha (transparency) component (0.0 to 1.0), default is 1.
        space: The color space, default is "rgb".

    Examples:
        >>> red = Color(1.0, 0.0, 0.0)
        >>> transparent_blue = Color(0.0, 0.0, 1.0, 0.5)
        >>> rgb255 = Color(255, 0, 128)  # Will be automatically normalized
    """
    red: int = 0
    green: int = 0
    blue: int = 0
    alpha: int = 1
    space: ColorSpace = "rgb"  # for future use

    def __post_init__(self):
        if self.red < 0 or self.red > 1:
            self.red = self.red / 255
        if self.green < 0 or self.green > 1:
            self.green = self.green / 255
        if self.blue < 0 or self.blue > 1:
            self.blue = self.blue / 255
        if self.alpha < 0 or self.alpha > 1:
            self.alpha = self.alpha / 255
        common_properties(self)

    def __str__(self):
        return f"Color({self.red}, {self.green}, {self.blue})"

    def __repr__(self):
        return f"Color({self.red}, {self.green}, {self.blue})"

    def copy(self):
        return Color(self.red, self.green, self.blue, self.alpha)

    @property
    def __key__(self):
        return (self.red, self.green, self.blue)

    def __hash__(self):
        return hash(self.__key__)

    @property
    def name(self):
        # search for the color in the named colors
        pass

    def __eq__(self, other):
        if isinstance(other, Color):
            return self.__key__ == other.__key__
        else:
            return False

    @property
    def rgb(self):
        return (self.red, self.green, self.blue)

    @property
    def rgba(self):
        return (self.red, self.green, self.blue, self.alpha)

    @property
    def rgb255(self):
        r, g, b = self.rgb
        if r > 1 or g > 1 or b > 1:
            return (r, g, b)
        return tuple(round(i * 255) for i in self.rgb)

    @property
    def rgba255(self):
        return tuple(round(i * 255) for i in self.rgba)


def blend(color1: Color, percent: int, color2: Color):
    """percent% of color1 and (100-percent)% of color2
    blended together to create a new color."""
    percent = percent / 100
    r1, g1, b1 = color1
    r2, g2, b2 = color2

    r_blend = r1 * percent + r2 * (1 - percent)
    g_blend = g1 * percent + g2 * (1 - percent)
    b_blend = b1 * percent + b2 * (1 - percent)

    return Color(r_blend, g_blend, b_blend)


def get_color(value):
    """
    if value is [r, g, b] return Color(r, g, b)
    if value is a string return Color(value)
    if value is a Color return value
    """
    if isinstance(value, Color):
        return value
    elif isinstance(value, str):
        return Color(value)
    elif isinstance(value, (list, tuple)):
        return Color(*value)
    else:
        raise TypeError("Invalid color value")


def check_color(color):
    if isinstance(color, Color):
        return color
    elif isinstance(color, (str, tuple, list)):
        return Color(*color)
    else:
        raise ValueError(
            f"Color must be a Color instance, a string, a tuple or a list. Got {color}"
        )


def rgb2hls(r, g, b):
    return rgb_to_hls(r, g, b)


def hls2rgb(h, l, s):
    return hls_to_rgb(h, l, s)


def rgb2hsv(r, g, b):
    return rgb_to_hsv(r, g, b)


def hsv2rgb(h, s, v):
    return hsv_to_rgb(h, s, v)


def rgb2yiq(r, g, b):
    return rgb_to_yiq(r, g, b)


def yiq2rgb(y, i, q):
    return yiq_to_rgb(y, i, q)


def rgb2hex(rgb):
    """Convert an RGB tuple to a hex color value."""
    r, g, b = rgb
    return f"#{r:02x}{g:02x}{b:02x}"


def hex2rgb(hex_val):
    """Convert a hex color value to an RGB tuple."""
    hex_val = hex_val.strip("#")
    return tuple(round(int(hex_val[i : i + 2], 16) / 255, 3) for i in (0, 2, 4))


def cmyk2rgb(c, m, y, k):
    """Convert a CMYK color value to an RGB tuple."""
    r = 1 - min(1, c * (1 - k) + k)
    g = 1 - min(1, m * (1 - k) + k)
    b = 1 - min(1, y * (1 - k) + k)
    return (r, g, b)


def random_color():
    """Return a random color."""
    return Color(random(), random(), random())


@dataclass
class LinearGradient:
    """A class representing a linear gradient.

    This class defines a linear gradient between two points with specified colors.

    Attributes:
        x1: The x-coordinate of the starting point.
        y1: The y-coordinate of the starting point.
        x2: The x-coordinate of the ending point.
        y2: The y-coordinate of the ending point.
        colors: A sequence of Color objects defining the gradient colors.
        positions: A sequence of Point objects defining the gradient positions.
        extend: Whether to extend the gradient beyond its endpoints.

    Examples:
        >>> from simetri.graphics.common import Point
        >>> gradient = LinearGradient(0, 0, 100, 100,
        ...                          [Color(1, 0, 0), Color(0, 0, 1)],
        ...                          [Point(0, 0), Point(100, 100)])
    """
    x1: float = 0.0
    y1: float = 0.0
    x2: float = 0.0
    y2: float = 0.0
    colors: Sequence[Color] = None
    positions: Sequence[Point] = None
    extend: bool = False

    def __post_init__(self):
        self.type = Types.GRADIENT
        self.subtype = Types.LINEAR
        common_properties(self)


@dataclass
class RadialGradient:
    """A class representing a radial gradient.

    This class defines a radial gradient that radiates outward from a center point.

    Attributes:
        x: The x-coordinate of the center point.
        y: The y-coordinate of the center point.
        radius: The radius of the gradient.
        colors: A sequence of Color objects defining the gradient colors.
        positions: A sequence of Point objects defining the gradient positions.
        extend: Whether to extend the gradient beyond its defined radius.

    Examples:
        >>> from simetri.graphics.common import Point
        >>> gradient = RadialGradient(50, 50, 30,
        ...                         [Color(1, 1, 1), Color(0, 0, 0)],
        ...                         [Point(50, 50), Point(80, 50)])
    """
    x: float = 0.0
    y: float = 0.0
    radius: float = 0.0
    colors: Sequence[Color] = None
    positions: Sequence[Point] = None
    extend: bool = False

    def __post_init__(self):
        self.type = Types.GRADIENT
        self.subtype = Types.RADIAL
        common_properties(self)


# <xcolor> TikZ library colors
# Apricot, Aquamarine, Bittersweet, Black, Blue, BlueGreen, BlueViolet, BrickRed, Brown, BurntOrange, CadetBlue,
# CarnationPink, Cerulean, CornflowerBlue, Cyan, Dandelion, DarkOrchid, Emerald, ForestGreen, Fuchsia, Goldenrod,
# Gray, Green, GreenYellow, JungleGreen, Lavender, LimeGreen, Magenta, Mahogany, Maroon, Melon, MidnightBlue,
# Mulberry, NavyBlue, OliveGreen, Orange, OrangeRed, Orchid, Peach, Periwinkle, PineGreen, Plum, ProcessBlue,
# Purple, RawSienna, Red, RedOrange, RedViolet, Rhodamine, RoyalBlue, RoyalPurple, RubineRed, Salmon, SeaGreen,
# Sepia, SkyBlue, SpringGreen, Tan, TealBlue, Thistle, Turquoise, Violet, VioletRed, White, WildStrawberry,
# Yellow, YellowGreen, YellowOrange


# Named colors from xkcd color survey

acid_green = Color(0.561, 0.996, 0.035)
adobe = Color(0.741, 0.424, 0.282)
algae = Color(0.329, 0.675, 0.408)
algae_green = Color(0.129, 0.765, 0.435)
almost_black = Color(0.027, 0.051, 0.051)
amber = Color(0.996, 0.702, 0.031)
amethyst = Color(0.608, 0.373, 0.753)
apple = Color(0.431, 0.796, 0.235)
apple_green = Color(0.463, 0.804, 0.149)
apricot = Color(1.0, 0.694, 0.427)
aqua = Color(0.075, 0.918, 0.788)
aqua_blue = Color(0.008, 0.847, 0.914)
aqua_green = Color(0.071, 0.882, 0.576)
aqua_marine = Color(0.18, 0.91, 0.733)
aquamarine = Color(0.016, 0.847, 0.698)
army_green = Color(0.294, 0.365, 0.086)
asparagus = Color(0.467, 0.671, 0.337)
aubergine = Color(0.239, 0.027, 0.204)
auburn = Color(0.604, 0.188, 0.004)
avocado = Color(0.565, 0.694, 0.204)
avocado_green = Color(0.529, 0.663, 0.133)
azul = Color(0.114, 0.365, 0.925)
azure = Color(0.024, 0.604, 0.953)
baby_blue = Color(0.635, 0.812, 0.996)
baby_green = Color(0.549, 1.0, 0.62)
baby_pink = Color(1.0, 0.718, 0.808)
baby_poo = Color(0.671, 0.565, 0.016)
baby_poop = Color(0.576, 0.486, 0.0)
baby_poop_green = Color(0.561, 0.596, 0.02)
baby_puke_green = Color(0.714, 0.769, 0.024)
baby_purple = Color(0.792, 0.608, 0.969)
baby_shit_brown = Color(0.678, 0.565, 0.051)
baby_shit_green = Color(0.533, 0.592, 0.09)
banana = Color(1.0, 1.0, 0.494)
banana_yellow = Color(0.98, 0.996, 0.294)
barbie_pink = Color(0.996, 0.275, 0.647)
barf_green = Color(0.58, 0.675, 0.008)
barney = Color(0.675, 0.114, 0.722)
barney_purple = Color(0.627, 0.016, 0.596)
battleship_grey = Color(0.42, 0.486, 0.522)
battleship_gray = Color(0.42, 0.486, 0.522)
beige = Color(0.902, 0.855, 0.651)
berry = Color(0.6, 0.059, 0.294)
bile = Color(0.71, 0.765, 0.024)
black = Color(0.0, 0.0, 0.0)
bland = Color(0.686, 0.659, 0.545)
blood = Color(0.467, 0.0, 0.004)
blood_orange = Color(0.996, 0.294, 0.012)
blood_red = Color(0.596, 0.0, 0.008)
blue = Color(0.012, 0.263, 0.875)
blue_blue = Color(0.133, 0.259, 0.78)
blue_green = Color(0.075, 0.494, 0.427)
blue_grey = Color(0.376, 0.486, 0.557)
blue_gray = Color(0.376, 0.486, 0.557)
blue_purple = Color(0.341, 0.161, 0.808)
blue_violet = Color(0.365, 0.024, 0.914)
blue_with_a_hint_of_purple = Color(0.325, 0.235, 0.776)
blue_purple = Color(0.353, 0.024, 0.937)
blueberry = Color(0.275, 0.255, 0.588)
bluegreen = Color(0.004, 0.478, 0.475)
bluegrey = Color(0.522, 0.639, 0.698)
bluegray = Color(0.522, 0.639, 0.698)
bluey_green = Color(0.169, 0.694, 0.475)
bluey_grey = Color(0.537, 0.627, 0.69)
bluey_gray = Color(0.537, 0.627, 0.69)
bluey_purple = Color(0.384, 0.255, 0.78)
bluish = Color(0.161, 0.463, 0.733)
bluish_green = Color(0.063, 0.651, 0.455)
bluish_grey = Color(0.455, 0.545, 0.592)
bluish_gray = Color(0.455, 0.545, 0.592)
bluish_purple = Color(0.439, 0.231, 0.906)
blurple = Color(0.333, 0.224, 0.8)
blush = Color(0.949, 0.62, 0.557)
blush_pink = Color(0.996, 0.51, 0.549)
booger = Color(0.608, 0.71, 0.235)
booger_green = Color(0.588, 0.706, 0.012)
bordeaux = Color(0.482, 0.0, 0.173)
boring_green = Color(0.388, 0.702, 0.396)
bottle_green = Color(0.016, 0.29, 0.02)
brick = Color(0.627, 0.212, 0.137)
brick_orange = Color(0.757, 0.29, 0.035)
brick_red = Color(0.561, 0.078, 0.008)
bright_aqua = Color(0.043, 0.976, 0.918)
bright_blue = Color(0.004, 0.396, 0.988)
bright_cyan = Color(0.255, 0.992, 0.996)
bright_green = Color(0.004, 1.0, 0.027)
bright_lavender = Color(0.78, 0.376, 1.0)
bright_light_blue = Color(0.149, 0.969, 0.992)
bright_light_green = Color(0.176, 0.996, 0.329)
bright_lilac = Color(0.788, 0.369, 0.984)
bright_lime = Color(0.529, 0.992, 0.02)
bright_lime_green = Color(0.396, 0.996, 0.031)
bright_magenta = Color(1.0, 0.031, 0.91)
bright_olive = Color(0.612, 0.733, 0.016)
bright_orange = Color(1.0, 0.357, 0.0)
bright_pink = Color(0.996, 0.004, 0.694)
bright_purple = Color(0.745, 0.012, 0.992)
bright_red = Color(1.0, 0.0, 0.051)
bright_sea_green = Color(0.02, 1.0, 0.651)
bright_sky_blue = Color(0.008, 0.8, 0.996)
bright_teal = Color(0.004, 0.976, 0.776)
bright_turquoise = Color(0.059, 0.996, 0.976)
bright_violet = Color(0.678, 0.039, 0.992)
bright_yellow = Color(1.0, 0.992, 0.004)
bright_yellow_green = Color(0.616, 1.0, 0.0)
british_racing_green = Color(0.02, 0.282, 0.051)
bronze = Color(0.659, 0.475, 0.0)
brown = Color(0.396, 0.216, 0.0)
brown_green = Color(0.439, 0.424, 0.067)
brown_grey = Color(0.553, 0.518, 0.408)
brown_gray = Color(0.553, 0.518, 0.408)
brown_orange = Color(0.725, 0.412, 0.008)
brown_red = Color(0.573, 0.169, 0.02)
brown_yellow = Color(0.698, 0.592, 0.02)
brownish = Color(0.612, 0.427, 0.341)
brownish_green = Color(0.416, 0.431, 0.035)
brownish_grey = Color(0.525, 0.467, 0.373)
brownish_gray = Color(0.525, 0.467, 0.373)
brownish_orange = Color(0.796, 0.467, 0.137)
brownish_pink = Color(0.761, 0.494, 0.475)
brownish_purple = Color(0.463, 0.259, 0.306)
brownish_red = Color(0.62, 0.212, 0.137)
brownish_yellow = Color(0.788, 0.69, 0.012)
browny_green = Color(0.435, 0.424, 0.039)
browny_orange = Color(0.792, 0.42, 0.008)
bruise = Color(0.494, 0.251, 0.443)
bubble_gum_pink = Color(1.0, 0.412, 0.686)
bubblegum = Color(1.0, 0.424, 0.71)
bubblegum_pink = Color(0.996, 0.514, 0.8)
buff = Color(0.996, 0.965, 0.62)
burgundy = Color(0.38, 0.0, 0.137)
burnt_orange = Color(0.753, 0.306, 0.004)
burnt_red = Color(0.624, 0.137, 0.02)
burnt_siena = Color(0.718, 0.322, 0.012)
burnt_sienna = Color(0.69, 0.306, 0.059)
burnt_umber = Color(0.627, 0.271, 0.055)
burnt_yellow = Color(0.835, 0.671, 0.035)
burple = Color(0.408, 0.196, 0.89)
butter = Color(1.0, 1.0, 0.506)
butter_yellow = Color(1.0, 0.992, 0.455)
butterscotch = Color(0.992, 0.694, 0.278)
cadet_blue = Color(0.306, 0.455, 0.588)
camel = Color(0.776, 0.624, 0.349)
camo = Color(0.498, 0.561, 0.306)
camo_green = Color(0.322, 0.396, 0.145)
camouflage_green = Color(0.294, 0.38, 0.075)
canary = Color(0.992, 1.0, 0.388)
canary_yellow = Color(1.0, 0.996, 0.251)
candy_pink = Color(1.0, 0.388, 0.914)
caramel = Color(0.686, 0.435, 0.035)
carmine = Color(0.616, 0.008, 0.086)
carnation = Color(0.992, 0.475, 0.561)
carnation_pink = Color(1.0, 0.498, 0.655)
carolina_blue = Color(0.541, 0.722, 0.996)
celadon = Color(0.745, 0.992, 0.718)
celery = Color(0.757, 0.992, 0.584)
cement = Color(0.647, 0.639, 0.569)
cerise = Color(0.871, 0.047, 0.384)
cerulean = Color(0.016, 0.522, 0.82)
cerulean_blue = Color(0.02, 0.431, 0.933)
charcoal = Color(0.204, 0.22, 0.216)
charcoal_grey = Color(0.235, 0.255, 0.259)
charcoal_gray = Color(0.235, 0.255, 0.259)
chartreuse = Color(0.757, 0.973, 0.039)
cherry = Color(0.812, 0.008, 0.204)
cherry_red = Color(0.969, 0.008, 0.165)
chestnut = Color(0.455, 0.157, 0.008)
chocolate = Color(0.239, 0.11, 0.008)
chocolate_brown = Color(0.255, 0.098, 0.0)
cinnamon = Color(0.675, 0.31, 0.024)
claret = Color(0.408, 0.0, 0.094)
clay = Color(0.714, 0.416, 0.314)
clay_brown = Color(0.698, 0.443, 0.239)
clear_blue = Color(0.141, 0.478, 0.992)
cloudy_blue = Color(0.675, 0.761, 0.851)
cobalt = Color(0.118, 0.282, 0.561)
cobalt_blue = Color(0.012, 0.039, 0.655)
cocoa = Color(0.529, 0.373, 0.259)
coffee = Color(0.651, 0.506, 0.298)
cool_blue = Color(0.286, 0.518, 0.722)
cool_green = Color(0.2, 0.722, 0.392)
cool_grey = Color(0.584, 0.639, 0.651)
cool_gray = Color(0.584, 0.639, 0.651)
copper = Color(0.714, 0.388, 0.145)
coral = Color(0.988, 0.353, 0.314)
coral_pink = Color(1.0, 0.38, 0.388)
cornflower = Color(0.416, 0.475, 0.969)
cornflower_blue = Color(0.318, 0.439, 0.843)
cranberry = Color(0.62, 0.0, 0.227)
cream = Color(1.0, 1.0, 0.761)
creme = Color(1.0, 1.0, 0.714)
crimson = Color(0.549, 0.0, 0.059)
custard = Color(1.0, 0.992, 0.471)
cyan = Color(0.0, 1.0, 1.0)
dandelion = Color(0.996, 0.875, 0.031)
dark = Color(0.106, 0.141, 0.192)
dark_aqua = Color(0.02, 0.412, 0.42)
dark_aquamarine = Color(0.004, 0.451, 0.443)
dark_beige = Color(0.675, 0.576, 0.384)
dark_blue = Color(0.0, 0.012, 0.357)
dark_blue_green = Color(0.0, 0.322, 0.286)
dark_blue_grey = Color(0.122, 0.231, 0.302)
dark_blue_gray = Color(0.122, 0.231, 0.302)
dark_brown = Color(0.204, 0.11, 0.008)
dark_coral = Color(0.812, 0.322, 0.306)
dark_cream = Color(1.0, 0.953, 0.604)
dark_cyan = Color(0.039, 0.533, 0.541)
dark_forest_green = Color(0.0, 0.176, 0.016)
dark_fuchsia = Color(0.616, 0.027, 0.349)
dark_gold = Color(0.71, 0.58, 0.063)
dark_grass_green = Color(0.22, 0.502, 0.016)
dark_green = Color(0.012, 0.208, 0.0)
dark_green_blue = Color(0.122, 0.388, 0.341)
dark_grey = Color(0.212, 0.216, 0.216)
dark_gray = Color(0.212, 0.216, 0.216)
dark_grey_blue = Color(0.161, 0.275, 0.357)
dark_gray_blue = Color(0.161, 0.275, 0.357)
dark_hot_pink = Color(0.851, 0.004, 0.4)
dark_indigo = Color(0.122, 0.035, 0.329)
dark_khaki = Color(0.608, 0.561, 0.333)
dark_lavender = Color(0.522, 0.404, 0.596)
dark_lilac = Color(0.612, 0.427, 0.647)
dark_lime = Color(0.518, 0.718, 0.004)
dark_lime_green = Color(0.494, 0.741, 0.004)
dark_magenta = Color(0.588, 0.0, 0.337)
dark_maroon = Color(0.235, 0.0, 0.031)
dark_mauve = Color(0.529, 0.298, 0.384)
dark_mint = Color(0.282, 0.753, 0.447)
dark_mint_green = Color(0.125, 0.753, 0.451)
dark_mustard = Color(0.659, 0.537, 0.02)
dark_navy = Color(0.0, 0.016, 0.208)
dark_navy_blue = Color(0.0, 0.008, 0.18)
dark_olive = Color(0.216, 0.243, 0.008)
dark_olive_green = Color(0.235, 0.302, 0.012)
dark_orange = Color(0.776, 0.318, 0.008)
dark_pastel_green = Color(0.337, 0.682, 0.341)
dark_peach = Color(0.871, 0.494, 0.365)
dark_periwinkle = Color(0.4, 0.373, 0.82)
dark_pink = Color(0.796, 0.255, 0.42)
dark_plum = Color(0.247, 0.004, 0.173)
dark_purple = Color(0.208, 0.024, 0.243)
dark_red = Color(0.518, 0.0, 0.0)
dark_rose = Color(0.71, 0.282, 0.365)
dark_royal_blue = Color(0.008, 0.024, 0.435)
dark_sage = Color(0.349, 0.522, 0.337)
dark_salmon = Color(0.784, 0.353, 0.325)
dark_sand = Color(0.659, 0.561, 0.349)
dark_sea_green = Color(0.067, 0.529, 0.365)
dark_seafoam = Color(0.122, 0.71, 0.478)
dark_seafoam_green = Color(0.243, 0.686, 0.463)
dark_sky_blue = Color(0.267, 0.557, 0.894)
dark_slate_blue = Color(0.129, 0.278, 0.38)
dark_tan = Color(0.686, 0.533, 0.29)
dark_taupe = Color(0.498, 0.408, 0.306)
dark_teal = Color(0.004, 0.302, 0.306)
dark_turquoise = Color(0.016, 0.361, 0.353)
dark_violet = Color(0.204, 0.004, 0.247)
dark_yellow = Color(0.835, 0.714, 0.039)
dark_yellow_green = Color(0.447, 0.561, 0.008)
darkblue = Color(0.012, 0.027, 0.392)
darkgreen = Color(0.02, 0.286, 0.027)
darkish_blue = Color(0.004, 0.255, 0.51)
darkish_green = Color(0.157, 0.486, 0.216)
darkish_pink = Color(0.855, 0.275, 0.49)
darkish_purple = Color(0.459, 0.098, 0.451)
darkish_red = Color(0.663, 0.012, 0.031)
deep_aqua = Color(0.031, 0.471, 0.498)
deep_blue = Color(0.016, 0.008, 0.451)
deep_brown = Color(0.255, 0.008, 0.0)
deep_green = Color(0.008, 0.349, 0.059)
deep_lavender = Color(0.553, 0.369, 0.718)
deep_lilac = Color(0.588, 0.431, 0.741)
deep_magenta = Color(0.627, 0.008, 0.361)
deep_orange = Color(0.863, 0.302, 0.004)
deep_pink = Color(0.796, 0.004, 0.384)
deep_purple = Color(0.212, 0.004, 0.247)
deep_red = Color(0.604, 0.008, 0.0)
deep_rose = Color(0.78, 0.278, 0.404)
deep_sea_blue = Color(0.004, 0.329, 0.51)
deep_sky_blue = Color(0.051, 0.459, 0.973)
deep_teal = Color(0.0, 0.333, 0.353)
deep_turquoise = Color(0.004, 0.451, 0.455)
deep_violet = Color(0.286, 0.024, 0.282)
denim = Color(0.231, 0.388, 0.549)
denim_blue = Color(0.231, 0.357, 0.573)
desert = Color(0.8, 0.678, 0.376)
diarrhea = Color(0.624, 0.514, 0.012)
dirt = Color(0.541, 0.431, 0.271)
dirt_brown = Color(0.514, 0.396, 0.224)
dirty_blue = Color(0.247, 0.51, 0.616)
dirty_green = Color(0.4, 0.494, 0.173)
dirty_orange = Color(0.784, 0.463, 0.024)
dirty_pink = Color(0.792, 0.482, 0.502)
dirty_purple = Color(0.451, 0.29, 0.396)
dirty_yellow = Color(0.804, 0.773, 0.039)
dodger_blue = Color(0.243, 0.51, 0.988)
drab = Color(0.51, 0.514, 0.267)
drab_green = Color(0.455, 0.584, 0.318)
dried_blood = Color(0.294, 0.004, 0.004)
duck_egg_blue = Color(0.765, 0.984, 0.957)
dull_blue = Color(0.286, 0.459, 0.612)
dull_brown = Color(0.529, 0.431, 0.294)
dull_green = Color(0.455, 0.651, 0.384)
dull_orange = Color(0.847, 0.525, 0.231)
dull_pink = Color(0.835, 0.525, 0.616)
dull_purple = Color(0.518, 0.349, 0.494)
dull_red = Color(0.733, 0.247, 0.247)
dull_teal = Color(0.373, 0.62, 0.561)
dull_yellow = Color(0.933, 0.863, 0.357)
dusk = Color(0.306, 0.329, 0.506)
dusk_blue = Color(0.149, 0.325, 0.553)
dusky_blue = Color(0.278, 0.373, 0.58)
dusky_pink = Color(0.8, 0.478, 0.545)
dusky_purple = Color(0.537, 0.357, 0.482)
dusky_rose = Color(0.729, 0.408, 0.451)
dust = Color(0.698, 0.6, 0.431)
dusty_blue = Color(0.353, 0.525, 0.678)
dusty_green = Color(0.463, 0.663, 0.451)
dusty_lavender = Color(0.675, 0.525, 0.659)
dusty_orange = Color(0.941, 0.514, 0.227)
dusty_pink = Color(0.835, 0.541, 0.58)
dusty_purple = Color(0.51, 0.373, 0.529)
dusty_red = Color(0.725, 0.282, 0.306)
dusty_rose = Color(0.753, 0.451, 0.478)
dusty_teal = Color(0.298, 0.565, 0.522)
earth = Color(0.635, 0.396, 0.243)
easter_green = Color(0.549, 0.992, 0.494)
easter_purple = Color(0.753, 0.443, 0.996)
ecru = Color(0.996, 1.0, 0.792)
egg_shell = Color(1.0, 0.988, 0.769)
eggplant = Color(0.22, 0.031, 0.208)
eggplant_purple = Color(0.263, 0.02, 0.255)
eggshell = Color(1.0, 1.0, 0.831)
eggshell_blue = Color(0.769, 1.0, 0.969)
electric_blue = Color(0.024, 0.322, 1.0)
electric_green = Color(0.129, 0.988, 0.051)
electric_lime = Color(0.659, 1.0, 0.016)
electric_pink = Color(1.0, 0.016, 0.565)
electric_purple = Color(0.667, 0.137, 1.0)
emerald = Color(0.004, 0.627, 0.286)
emerald_green = Color(0.008, 0.561, 0.118)
evergreen = Color(0.02, 0.278, 0.165)
faded_blue = Color(0.396, 0.549, 0.733)
faded_green = Color(0.482, 0.698, 0.455)
faded_orange = Color(0.941, 0.58, 0.302)
faded_pink = Color(0.871, 0.616, 0.675)
faded_purple = Color(0.569, 0.431, 0.6)
faded_red = Color(0.827, 0.286, 0.306)
faded_yellow = Color(0.996, 1.0, 0.498)
fawn = Color(0.812, 0.686, 0.482)
fern = Color(0.388, 0.663, 0.314)
fern_green = Color(0.329, 0.553, 0.267)
fire_engine_red = Color(0.996, 0.0, 0.008)
flat_blue = Color(0.235, 0.451, 0.659)
flat_green = Color(0.412, 0.616, 0.298)
fluorescent_green = Color(0.031, 1.0, 0.031)
fluro_green = Color(0.039, 1.0, 0.008)
foam_green = Color(0.565, 0.992, 0.663)
forest = Color(0.043, 0.333, 0.035)
forest_green = Color(0.024, 0.278, 0.047)
forrest_green = Color(0.082, 0.267, 0.024)
french_blue = Color(0.263, 0.42, 0.678)
fresh_green = Color(0.412, 0.847, 0.31)
frog_green = Color(0.345, 0.737, 0.031)
fuchsia = Color(0.929, 0.051, 0.851)
gold = Color(0.859, 0.706, 0.047)
golden = Color(0.961, 0.749, 0.012)
golden_brown = Color(0.698, 0.478, 0.004)
golden_rod = Color(0.976, 0.737, 0.031)
golden_yellow = Color(0.996, 0.776, 0.082)
goldenrod = Color(0.98, 0.761, 0.02)
grape = Color(0.424, 0.204, 0.38)
grape_purple = Color(0.365, 0.078, 0.318)
grapefruit = Color(0.992, 0.349, 0.337)
grass = Color(0.361, 0.675, 0.176)
grass_green = Color(0.247, 0.608, 0.043)
grassy_green = Color(0.255, 0.612, 0.012)
green = Color(0.082, 0.69, 0.102)
green_apple = Color(0.369, 0.863, 0.122)
green_blue = Color(0.024, 0.706, 0.545)
green_brown = Color(0.329, 0.306, 0.012)
green_grey = Color(0.467, 0.573, 0.435)
green_gray = Color(0.467, 0.573, 0.435)
green_teal = Color(0.047, 0.71, 0.467)
green_yellow = Color(0.788, 1.0, 0.153)
green_blue = Color(0.004, 0.753, 0.553)
green_yellow = Color(0.71, 0.808, 0.031)
greenblue = Color(0.137, 0.769, 0.545)
greenish = Color(0.251, 0.639, 0.408)
greenish_beige = Color(0.788, 0.82, 0.475)
greenish_blue = Color(0.043, 0.545, 0.529)
greenish_brown = Color(0.412, 0.38, 0.071)
greenish_cyan = Color(0.165, 0.996, 0.718)
greenish_grey = Color(0.588, 0.682, 0.553)
greenish_gray = Color(0.588, 0.682, 0.553)
greenish_tan = Color(0.737, 0.796, 0.478)
greenish_teal = Color(0.196, 0.749, 0.518)
greenish_turquoise = Color(0.0, 0.984, 0.69)
greenish_yellow = Color(0.804, 0.992, 0.008)
greeny_blue = Color(0.259, 0.702, 0.584)
greeny_brown = Color(0.412, 0.376, 0.024)
greeny_grey = Color(0.494, 0.627, 0.478)
greeny_gray = Color(0.494, 0.627, 0.478)
greeny_yellow = Color(0.776, 0.973, 0.031)
grey = Color(0.573, 0.584, 0.569)
gray = Color(0.573, 0.584, 0.569)
grey_blue = Color(0.42, 0.545, 0.643)
gray_blue = Color(0.42, 0.545, 0.643)
grey_brown = Color(0.498, 0.439, 0.325)
gray_brown = Color(0.498, 0.439, 0.325)
grey_green = Color(0.471, 0.608, 0.451)
gray_green = Color(0.471, 0.608, 0.451)
grey_pink = Color(0.765, 0.565, 0.608)
gray_pink = Color(0.765, 0.565, 0.608)
grey_purple = Color(0.51, 0.427, 0.549)
gray_purple = Color(0.51, 0.427, 0.549)
grey_teal = Color(0.369, 0.608, 0.541)
gray_teal = Color(0.369, 0.608, 0.541)
grey_blue = Color(0.392, 0.49, 0.557)
gray_blue = Color(0.392, 0.49, 0.557)
grey_green = Color(0.525, 0.631, 0.49)
gray_green = Color(0.525, 0.631, 0.49)
greyblue = Color(0.467, 0.631, 0.71)
grayblue = Color(0.467, 0.631, 0.71)
greyish = Color(0.659, 0.643, 0.584)
grayish = Color(0.659, 0.643, 0.584)
greyish_blue = Color(0.369, 0.506, 0.616)
grayish_blue = Color(0.369, 0.506, 0.616)
greyish_brown = Color(0.478, 0.416, 0.31)
grayish_brown = Color(0.478, 0.416, 0.31)
greyish_green = Color(0.51, 0.651, 0.49)
grayish_green = Color(0.51, 0.651, 0.49)
greyish_pink = Color(0.784, 0.553, 0.58)
grayish_pink = Color(0.784, 0.553, 0.58)
greyish_purple = Color(0.533, 0.443, 0.569)
grayish_purple = Color(0.533, 0.443, 0.569)
greyish_teal = Color(0.443, 0.624, 0.569)
grayish_teal = Color(0.443, 0.624, 0.569)
gross_green = Color(0.627, 0.749, 0.086)
gunmetal = Color(0.325, 0.384, 0.404)
hazel = Color(0.557, 0.463, 0.094)
heather = Color(0.643, 0.518, 0.675)
heliotrope = Color(0.851, 0.31, 0.961)
highlighter_green = Color(0.106, 0.988, 0.024)
hospital_green = Color(0.608, 0.898, 0.667)
hot_green = Color(0.145, 1.0, 0.161)
hot_magenta = Color(0.961, 0.016, 0.788)
hot_pink = Color(1.0, 0.008, 0.553)
hot_purple = Color(0.796, 0.0, 0.961)
hunter_green = Color(0.043, 0.251, 0.031)
ice = Color(0.839, 1.0, 0.98)
ice_blue = Color(0.843, 1.0, 0.996)
icky_green = Color(0.561, 0.682, 0.133)
indian_red = Color(0.522, 0.055, 0.016)
indigo = Color(0.22, 0.008, 0.51)
indigo_blue = Color(0.227, 0.094, 0.694)
iris = Color(0.384, 0.345, 0.769)
irish_green = Color(0.004, 0.584, 0.161)
ivory = Color(1.0, 1.0, 0.796)
jade = Color(0.122, 0.655, 0.455)
jade_green = Color(0.169, 0.686, 0.416)
jungle_green = Color(0.016, 0.51, 0.263)
kelley_green = Color(0.0, 0.576, 0.216)
kelly_green = Color(0.008, 0.671, 0.18)
kermit_green = Color(0.361, 0.698, 0.0)
key_lime = Color(0.682, 1.0, 0.431)
khaki = Color(0.667, 0.651, 0.384)
khaki_green = Color(0.447, 0.525, 0.224)
kiwi = Color(0.612, 0.937, 0.263)
kiwi_green = Color(0.557, 0.898, 0.247)
lavender = Color(0.78, 0.624, 0.937)
lavender_blue = Color(0.545, 0.533, 0.973)
lavender_pink = Color(0.867, 0.522, 0.843)
lawn_green = Color(0.302, 0.643, 0.035)
leaf = Color(0.443, 0.667, 0.204)
leaf_green = Color(0.361, 0.663, 0.016)
leafy_green = Color(0.318, 0.718, 0.231)
leather = Color(0.675, 0.455, 0.204)
lemon = Color(0.992, 1.0, 0.322)
lemon_green = Color(0.678, 0.973, 0.008)
lemon_lime = Color(0.749, 0.996, 0.157)
lemon_yellow = Color(0.992, 1.0, 0.22)
lichen = Color(0.561, 0.714, 0.482)
light_aqua = Color(0.549, 1.0, 0.859)
light_aquamarine = Color(0.482, 0.992, 0.78)
light_beige = Color(1.0, 0.996, 0.714)
light_blue = Color(0.584, 0.816, 0.988)
light_blue_green = Color(0.494, 0.984, 0.702)
light_blue_grey = Color(0.718, 0.788, 0.886)
light_blue_gray = Color(0.718, 0.788, 0.886)
light_bluish_green = Color(0.463, 0.992, 0.659)
light_bright_green = Color(0.325, 0.996, 0.361)
light_brown = Color(0.678, 0.506, 0.314)
light_burgundy = Color(0.659, 0.255, 0.357)
light_cyan = Color(0.675, 1.0, 0.988)
light_eggplant = Color(0.537, 0.271, 0.522)
light_forest_green = Color(0.31, 0.569, 0.325)
light_gold = Color(0.992, 0.863, 0.361)
light_grass_green = Color(0.604, 0.969, 0.392)
light_green = Color(0.588, 0.976, 0.482)
light_green_blue = Color(0.337, 0.988, 0.635)
light_greenish_blue = Color(0.388, 0.969, 0.706)
light_grey = Color(0.847, 0.863, 0.839)
light_gray = Color(0.847, 0.863, 0.839)
light_grey_blue = Color(0.616, 0.737, 0.831)
light_gray_blue = Color(0.616, 0.737, 0.831)
light_grey_green = Color(0.718, 0.882, 0.631)
light_gray_green = Color(0.718, 0.882, 0.631)
light_indigo = Color(0.427, 0.353, 0.812)
light_khaki = Color(0.902, 0.949, 0.635)
light_lavendar = Color(0.937, 0.753, 0.996)
light_lavender = Color(0.875, 0.773, 0.996)
light_light_blue = Color(0.792, 1.0, 0.984)
light_light_green = Color(0.784, 1.0, 0.69)
light_lilac = Color(0.929, 0.784, 1.0)
light_lime = Color(0.682, 0.992, 0.424)
light_lime_green = Color(0.725, 1.0, 0.4)
light_magenta = Color(0.98, 0.373, 0.969)
light_maroon = Color(0.635, 0.282, 0.341)
light_mauve = Color(0.761, 0.573, 0.631)
light_mint = Color(0.714, 1.0, 0.733)
light_mint_green = Color(0.651, 0.984, 0.698)
light_moss_green = Color(0.651, 0.784, 0.459)
light_mustard = Color(0.969, 0.835, 0.376)
light_navy = Color(0.082, 0.314, 0.518)
light_navy_blue = Color(0.18, 0.353, 0.533)
light_neon_green = Color(0.306, 0.992, 0.329)
light_olive = Color(0.675, 0.749, 0.412)
light_olive_green = Color(0.643, 0.745, 0.361)
light_orange = Color(0.992, 0.667, 0.282)
light_pastel_green = Color(0.698, 0.984, 0.647)
light_pea_green = Color(0.769, 0.996, 0.51)
light_peach = Color(1.0, 0.847, 0.694)
light_periwinkle = Color(0.757, 0.776, 0.988)
light_pink = Color(1.0, 0.82, 0.875)
light_plum = Color(0.616, 0.341, 0.514)
light_purple = Color(0.749, 0.467, 0.965)
light_red = Color(1.0, 0.278, 0.298)
light_rose = Color(1.0, 0.773, 0.796)
light_royal_blue = Color(0.227, 0.18, 0.996)
light_sage = Color(0.737, 0.925, 0.675)
light_salmon = Color(0.996, 0.663, 0.576)
light_sea_green = Color(0.596, 0.965, 0.69)
light_seafoam = Color(0.627, 0.996, 0.749)
light_seafoam_green = Color(0.655, 1.0, 0.71)
light_sky_blue = Color(0.776, 0.988, 1.0)
light_tan = Color(0.984, 0.933, 0.675)
light_teal = Color(0.565, 0.894, 0.757)
light_turquoise = Color(0.494, 0.957, 0.8)
light_urple = Color(0.702, 0.435, 0.965)
light_violet = Color(0.839, 0.706, 0.988)
light_yellow = Color(1.0, 0.996, 0.478)
light_yellow_green = Color(0.8, 0.992, 0.498)
light_yellowish_green = Color(0.761, 1.0, 0.537)
lightblue = Color(0.482, 0.784, 0.965)
lighter_green = Color(0.459, 0.992, 0.388)
lighter_purple = Color(0.647, 0.353, 0.957)
lightgreen = Color(0.463, 1.0, 0.482)
lightish_blue = Color(0.239, 0.478, 0.992)
lightish_green = Color(0.38, 0.882, 0.376)
lightish_purple = Color(0.647, 0.322, 0.902)
lightish_red = Color(0.996, 0.184, 0.29)
lilac = Color(0.808, 0.635, 0.992)
liliac = Color(0.769, 0.557, 0.992)
lime = Color(0.667, 1.0, 0.196)
lime_green = Color(0.537, 0.996, 0.02)
lime_yellow = Color(0.816, 0.996, 0.114)
lipstick = Color(0.835, 0.09, 0.306)
lipstick_red = Color(0.753, 0.008, 0.184)
macaroni_and_cheese = Color(0.937, 0.706, 0.208)
magenta = Color(0.761, 0.0, 0.471)
mahogany = Color(0.29, 0.004, 0.0)
maize = Color(0.957, 0.816, 0.329)
mango = Color(1.0, 0.651, 0.169)
manilla = Color(1.0, 0.98, 0.525)
marigold = Color(0.988, 0.753, 0.024)
marine = Color(0.016, 0.18, 0.376)
marine_blue = Color(0.004, 0.22, 0.416)
maroon = Color(0.396, 0.0, 0.129)
mauve = Color(0.682, 0.443, 0.506)
medium_blue = Color(0.173, 0.435, 0.733)
medium_brown = Color(0.498, 0.318, 0.071)
medium_green = Color(0.224, 0.678, 0.282)
medium_grey = Color(0.49, 0.498, 0.486)
medium_gray = Color(0.49, 0.498, 0.486)
medium_pink = Color(0.953, 0.38, 0.588)
medium_purple = Color(0.62, 0.263, 0.635)
melon = Color(1.0, 0.471, 0.333)
merlot = Color(0.451, 0.0, 0.224)
metallic_blue = Color(0.31, 0.451, 0.557)
mid_blue = Color(0.153, 0.416, 0.702)
mid_green = Color(0.314, 0.655, 0.278)
midnight = Color(0.012, 0.004, 0.176)
midnight_blue = Color(0.008, 0.0, 0.208)
midnight_purple = Color(0.157, 0.004, 0.216)
military_green = Color(0.4, 0.486, 0.243)
milk_chocolate = Color(0.498, 0.306, 0.118)
mint = Color(0.624, 0.996, 0.69)
mint_green = Color(0.561, 1.0, 0.624)
minty_green = Color(0.043, 0.969, 0.49)
mocha = Color(0.616, 0.463, 0.318)
moss = Color(0.463, 0.6, 0.345)
moss_green = Color(0.396, 0.545, 0.22)
mossy_green = Color(0.388, 0.545, 0.153)
mud = Color(0.451, 0.361, 0.071)
mud_brown = Color(0.376, 0.275, 0.059)
mud_green = Color(0.376, 0.4, 0.008)
muddy_brown = Color(0.533, 0.408, 0.024)
muddy_green = Color(0.396, 0.455, 0.196)
muddy_yellow = Color(0.749, 0.675, 0.02)
mulberry = Color(0.573, 0.039, 0.306)
murky_green = Color(0.424, 0.478, 0.055)
mushroom = Color(0.729, 0.62, 0.533)
mustard = Color(0.808, 0.702, 0.004)
mustard_brown = Color(0.675, 0.494, 0.016)
mustard_green = Color(0.659, 0.71, 0.016)
mustard_yellow = Color(0.824, 0.741, 0.039)
muted_blue = Color(0.231, 0.443, 0.624)
muted_green = Color(0.373, 0.627, 0.322)
muted_pink = Color(0.82, 0.463, 0.561)
muted_purple = Color(0.502, 0.357, 0.529)
nasty_green = Color(0.439, 0.698, 0.247)
navy = Color(0.004, 0.082, 0.243)
navy_blue = Color(0.0, 0.067, 0.275)
navy_green = Color(0.208, 0.325, 0.039)
neon_blue = Color(0.016, 0.851, 1.0)
neon_green = Color(0.047, 1.0, 0.047)
neon_pink = Color(0.996, 0.004, 0.604)
neon_purple = Color(0.737, 0.075, 0.996)
neon_red = Color(1.0, 0.027, 0.227)
neon_yellow = Color(0.812, 1.0, 0.016)
nice_blue = Color(0.063, 0.478, 0.69)
night_blue = Color(0.016, 0.012, 0.282)
ocean = Color(0.004, 0.482, 0.573)
ocean_blue = Color(0.012, 0.443, 0.612)
ocean_green = Color(0.239, 0.6, 0.451)
ocher = Color(0.749, 0.608, 0.047)
ochre = Color(0.749, 0.565, 0.02)
ocre = Color(0.776, 0.612, 0.016)
off_blue = Color(0.337, 0.518, 0.682)
off_green = Color(0.42, 0.639, 0.325)
off_white = Color(1.0, 1.0, 0.894)
off_yellow = Color(0.945, 0.953, 0.247)
old_pink = Color(0.78, 0.475, 0.525)
old_rose = Color(0.784, 0.498, 0.537)
olive = Color(0.431, 0.459, 0.055)
olive_brown = Color(0.392, 0.329, 0.012)
olive_drab = Color(0.435, 0.463, 0.196)
olive_green = Color(0.404, 0.478, 0.016)
olive_yellow = Color(0.761, 0.718, 0.035)
orange = Color(0.976, 0.451, 0.024)
orange_brown = Color(0.745, 0.392, 0.0)
orange_pink = Color(1.0, 0.435, 0.322)
orange_red = Color(0.992, 0.255, 0.118)
orange_yellow = Color(1.0, 0.678, 0.004)
orangeish = Color(0.992, 0.553, 0.286)
orangered = Color(0.996, 0.259, 0.059)
orangey_brown = Color(0.694, 0.376, 0.008)
orangey_red = Color(0.98, 0.259, 0.141)
orangey_yellow = Color(0.992, 0.725, 0.082)
orangish = Color(0.988, 0.51, 0.29)
orangish_brown = Color(0.698, 0.373, 0.012)
orangish_red = Color(0.957, 0.212, 0.02)
orchid = Color(0.784, 0.459, 0.769)
pale = Color(1.0, 0.976, 0.816)
pale_aqua = Color(0.722, 1.0, 0.922)
pale_blue = Color(0.816, 0.996, 0.996)
pale_brown = Color(0.694, 0.569, 0.431)
pale_cyan = Color(0.718, 1.0, 0.98)
pale_gold = Color(0.992, 0.871, 0.424)
pale_green = Color(0.78, 0.992, 0.71)
pale_grey = Color(0.992, 0.992, 0.996)
pale_gray = Color(0.992, 0.992, 0.996)
pale_lavender = Color(0.933, 0.812, 0.996)
pale_light_green = Color(0.694, 0.988, 0.6)
pale_lilac = Color(0.894, 0.796, 1.0)
pale_lime = Color(0.745, 0.992, 0.451)
pale_lime_green = Color(0.694, 1.0, 0.396)
pale_magenta = Color(0.843, 0.404, 0.678)
pale_mauve = Color(0.996, 0.816, 0.988)
pale_olive = Color(0.725, 0.8, 0.506)
pale_olive_green = Color(0.694, 0.824, 0.482)
pale_orange = Color(1.0, 0.655, 0.337)
pale_peach = Color(1.0, 0.898, 0.678)
pale_pink = Color(1.0, 0.812, 0.863)
pale_purple = Color(0.718, 0.565, 0.831)
pale_red = Color(0.851, 0.329, 0.302)
pale_rose = Color(0.992, 0.757, 0.773)
pale_salmon = Color(1.0, 0.694, 0.604)
pale_sky_blue = Color(0.741, 0.965, 0.996)
pale_teal = Color(0.51, 0.796, 0.698)
pale_turquoise = Color(0.647, 0.984, 0.835)
pale_violet = Color(0.808, 0.682, 0.98)
pale_yellow = Color(1.0, 1.0, 0.518)
parchment = Color(0.996, 0.988, 0.686)
pastel_blue = Color(0.635, 0.749, 0.996)
pastel_green = Color(0.69, 1.0, 0.616)
pastel_orange = Color(1.0, 0.588, 0.31)
pastel_pink = Color(1.0, 0.729, 0.804)
pastel_purple = Color(0.792, 0.627, 1.0)
pastel_red = Color(0.859, 0.345, 0.337)
pastel_yellow = Color(1.0, 0.996, 0.443)
pea = Color(0.643, 0.749, 0.125)
pea_green = Color(0.557, 0.671, 0.071)
pea_soup = Color(0.573, 0.6, 0.004)
pea_soup_green = Color(0.58, 0.651, 0.09)
peach = Color(1.0, 0.69, 0.486)
peachy_pink = Color(1.0, 0.604, 0.541)
peacock_blue = Color(0.004, 0.404, 0.584)
pear = Color(0.796, 0.973, 0.373)
periwinkle = Color(0.557, 0.51, 0.996)
periwinkle_blue = Color(0.561, 0.6, 0.984)
perrywinkle = Color(0.561, 0.549, 0.906)
petrol = Color(0.0, 0.373, 0.416)
pig_pink = Color(0.906, 0.557, 0.647)
pine = Color(0.169, 0.365, 0.204)
pine_green = Color(0.039, 0.282, 0.118)
pink = Color(1.0, 0.506, 0.753)
pink_purple = Color(0.859, 0.294, 0.855)
pink_red = Color(0.961, 0.02, 0.31)
pink_purple = Color(0.937, 0.114, 0.906)
pinkish = Color(0.831, 0.416, 0.494)
pinkish_brown = Color(0.694, 0.447, 0.38)
pinkish_grey = Color(0.784, 0.675, 0.663)
pinkish_gray = Color(0.784, 0.675, 0.663)
pinkish_orange = Color(1.0, 0.447, 0.298)
pinkish_purple = Color(0.839, 0.282, 0.843)
pinkish_red = Color(0.945, 0.047, 0.271)
pinkish_tan = Color(0.851, 0.608, 0.51)
pinky = Color(0.988, 0.525, 0.667)
pinky_purple = Color(0.788, 0.298, 0.745)
pinky_red = Color(0.988, 0.149, 0.278)
piss_yellow = Color(0.867, 0.839, 0.094)
pistachio = Color(0.753, 0.98, 0.545)
plum = Color(0.345, 0.059, 0.255)
plum_purple = Color(0.306, 0.02, 0.314)
poison_green = Color(0.251, 0.992, 0.078)
poo = Color(0.561, 0.451, 0.012)
poo_brown = Color(0.533, 0.373, 0.004)
poop = Color(0.498, 0.369, 0.0)
poop_brown = Color(0.478, 0.349, 0.004)
poop_green = Color(0.435, 0.486, 0.0)
powder_blue = Color(0.694, 0.82, 0.988)
powder_pink = Color(1.0, 0.698, 0.816)
primary_blue = Color(0.031, 0.016, 0.976)
prussian_blue = Color(0.0, 0.271, 0.467)
puce = Color(0.647, 0.494, 0.322)
puke = Color(0.647, 0.647, 0.008)
puke_brown = Color(0.58, 0.467, 0.024)
puke_green = Color(0.604, 0.682, 0.027)
puke_yellow = Color(0.761, 0.745, 0.055)
pumpkin = Color(0.882, 0.467, 0.004)
pumpkin_orange = Color(0.984, 0.49, 0.027)
pure_blue = Color(0.008, 0.012, 0.886)
purple = Color(0.494, 0.118, 0.612)
purple_blue = Color(0.388, 0.176, 0.914)
purple_brown = Color(0.404, 0.227, 0.247)
purple_grey = Color(0.525, 0.435, 0.522)
purple_gray = Color(0.525, 0.435, 0.522)
purple_pink = Color(0.878, 0.247, 0.847)
purple_red = Color(0.6, 0.004, 0.278)
purple_blue = Color(0.365, 0.129, 0.816)
purple_pink = Color(0.843, 0.145, 0.871)
purpleish = Color(0.596, 0.337, 0.553)
purpleish_blue = Color(0.38, 0.251, 0.937)
purpleish_pink = Color(0.875, 0.306, 0.784)
purpley = Color(0.529, 0.337, 0.894)
purpley_blue = Color(0.373, 0.204, 0.906)
purpley_grey = Color(0.58, 0.494, 0.58)
purpley_gray = Color(0.58, 0.494, 0.58)
purpley_pink = Color(0.784, 0.235, 0.725)
purplish = Color(0.58, 0.337, 0.549)
purplish_blue = Color(0.376, 0.118, 0.976)
purplish_brown = Color(0.42, 0.259, 0.278)
purplish_grey = Color(0.478, 0.408, 0.498)
purplisth_gray = Color(0.478, 0.408, 0.498)
purplish_pink = Color(0.808, 0.365, 0.682)
purplish_red = Color(0.69, 0.02, 0.294)
purply = Color(0.596, 0.247, 0.698)
purply_blue = Color(0.4, 0.102, 0.933)
purply_pink = Color(0.941, 0.459, 0.902)
putty = Color(0.745, 0.682, 0.541)
racing_green = Color(0.004, 0.275, 0.0)
radioactive_green = Color(0.173, 0.98, 0.122)
raspberry = Color(0.69, 0.004, 0.286)
raw_sienna = Color(0.604, 0.384, 0.0)
raw_umber = Color(0.655, 0.369, 0.035)
really_light_blue = Color(0.831, 1.0, 1.0)
red = Color(0.898, 0.0, 0.0)
red_brown = Color(0.545, 0.18, 0.086)
red_orange = Color(0.992, 0.235, 0.024)
red_pink = Color(0.98, 0.165, 0.333)
red_purple = Color(0.51, 0.027, 0.278)
red_violet = Color(0.62, 0.004, 0.408)
red_wine = Color(0.549, 0.0, 0.204)
reddish = Color(0.769, 0.259, 0.251)
reddish_brown = Color(0.498, 0.169, 0.039)
reddish_grey = Color(0.6, 0.459, 0.439)
reddish_gray = Color(0.6, 0.459, 0.439)
reddish_orange = Color(0.973, 0.282, 0.11)
reddish_pink = Color(0.996, 0.173, 0.329)
reddish_purple = Color(0.569, 0.035, 0.318)
reddy_brown = Color(0.431, 0.063, 0.02)
rich_blue = Color(0.008, 0.106, 0.976)
rich_purple = Color(0.447, 0.0, 0.345)
robin_egg_blue = Color(0.541, 0.945, 0.996)
robins_egg = Color(0.427, 0.929, 0.992)
robins_egg_blue = Color(0.596, 0.937, 0.976)
rosa = Color(0.996, 0.525, 0.643)
rose = Color(0.812, 0.384, 0.459)
rose_pink = Color(0.969, 0.529, 0.604)
rose_red = Color(0.745, 0.004, 0.235)
rosy_pink = Color(0.965, 0.408, 0.557)
rouge = Color(0.671, 0.071, 0.224)
royal = Color(0.047, 0.09, 0.576)
royal_blue = Color(0.02, 0.016, 0.667)
royal_purple = Color(0.294, 0.0, 0.431)
ruby = Color(0.792, 0.004, 0.278)
russet = Color(0.631, 0.224, 0.02)
rust = Color(0.659, 0.235, 0.035)
rust_brown = Color(0.545, 0.192, 0.012)
rust_orange = Color(0.769, 0.333, 0.031)
rust_red = Color(0.667, 0.153, 0.016)
rusty_orange = Color(0.804, 0.349, 0.035)
rusty_red = Color(0.686, 0.184, 0.051)
saffron = Color(0.996, 0.698, 0.035)
sage = Color(0.529, 0.682, 0.451)
sage_green = Color(0.533, 0.702, 0.471)
salmon = Color(1.0, 0.475, 0.424)
salmon_pink = Color(0.996, 0.482, 0.486)
sand = Color(0.886, 0.792, 0.463)
sand_brown = Color(0.796, 0.647, 0.376)
sand_yellow = Color(0.988, 0.882, 0.4)
sandstone = Color(0.788, 0.682, 0.455)
sandy = Color(0.945, 0.855, 0.478)
sandy_brown = Color(0.769, 0.651, 0.38)
sandy_yellow = Color(0.992, 0.933, 0.451)
sap_green = Color(0.361, 0.545, 0.082)
sapphire = Color(0.129, 0.22, 0.671)
scarlet = Color(0.745, 0.004, 0.098)
sea = Color(0.235, 0.6, 0.573)
sea_blue = Color(0.016, 0.455, 0.584)
sea_green = Color(0.325, 0.988, 0.631)
seafoam = Color(0.502, 0.976, 0.678)
seafoam_blue = Color(0.471, 0.82, 0.714)
seafoam_green = Color(0.478, 0.976, 0.671)
seaweed = Color(0.094, 0.82, 0.482)
seaweed_green = Color(0.208, 0.678, 0.42)
sepia = Color(0.596, 0.369, 0.169)
shamrock = Color(0.004, 0.706, 0.298)
shamrock_green = Color(0.008, 0.757, 0.302)
shit = Color(0.498, 0.373, 0.0)
shit_brown = Color(0.482, 0.345, 0.016)
shit_green = Color(0.459, 0.502, 0.0)
shocking_pink = Color(0.996, 0.008, 0.635)
sick_green = Color(0.616, 0.725, 0.173)
sickly_green = Color(0.58, 0.698, 0.11)
sickly_yellow = Color(0.816, 0.894, 0.161)
sienna = Color(0.663, 0.337, 0.118)
silver = Color(0.773, 0.788, 0.78)
sky = Color(0.51, 0.792, 0.988)
sky_blue = Color(0.459, 0.733, 0.992)
slate = Color(0.318, 0.396, 0.447)
slate_blue = Color(0.357, 0.486, 0.6)
slate_green = Color(0.396, 0.553, 0.427)
slate_grey = Color(0.349, 0.396, 0.427)
slate_gray = Color(0.349, 0.396, 0.427)
slime_green = Color(0.6, 0.8, 0.016)
snot = Color(0.675, 0.733, 0.051)
snot_green = Color(0.616, 0.757, 0.0)
soft_blue = Color(0.392, 0.533, 0.918)
soft_green = Color(0.435, 0.761, 0.463)
soft_pink = Color(0.992, 0.69, 0.753)
soft_purple = Color(0.651, 0.435, 0.71)
spearmint = Color(0.118, 0.973, 0.463)
spring_green = Color(0.663, 0.976, 0.443)
spruce = Color(0.039, 0.373, 0.22)
squash = Color(0.949, 0.671, 0.082)
steel = Color(0.451, 0.522, 0.584)
steel_blue = Color(0.353, 0.49, 0.604)
steel_grey = Color(0.435, 0.51, 0.541)
steel_gray = Color(0.435, 0.51, 0.541)
stone = Color(0.678, 0.647, 0.529)
stormy_blue = Color(0.314, 0.482, 0.612)
straw = Color(0.988, 0.965, 0.475)
strawberry = Color(0.984, 0.161, 0.263)
strong_blue = Color(0.047, 0.024, 0.969)
strong_pink = Color(1.0, 0.027, 0.537)
sun_yellow = Color(1.0, 0.875, 0.133)
sunflower = Color(1.0, 0.773, 0.071)
sunflower_yellow = Color(1.0, 0.855, 0.012)
sunny_yellow = Color(1.0, 0.976, 0.09)
sunshine_yellow = Color(1.0, 0.992, 0.216)
swamp = Color(0.412, 0.514, 0.224)
swamp_green = Color(0.455, 0.522, 0.0)
tan_ = Color(0.82, 0.698, 0.435) # tan is a reserved word
tan_brown = Color(0.671, 0.494, 0.298)
tan_green = Color(0.663, 0.745, 0.439)
tangerine = Color(1.0, 0.58, 0.031)
taupe = Color(0.725, 0.635, 0.506)
tea = Color(0.396, 0.671, 0.486)
tea_green = Color(0.741, 0.973, 0.639)
teal = Color(0.008, 0.576, 0.525)
teal_blue = Color(0.004, 0.533, 0.624)
teal_green = Color(0.145, 0.639, 0.435)
tealish = Color(0.141, 0.737, 0.659)
tealish_green = Color(0.047, 0.863, 0.451)
terra_cotta = Color(0.788, 0.392, 0.231)
terracota = Color(0.796, 0.408, 0.263)
terracotta = Color(0.792, 0.4, 0.255)
tiffany_blue = Color(0.482, 0.949, 0.855)
tomato = Color(0.937, 0.251, 0.149)
tomato_red = Color(0.925, 0.176, 0.004)
topaz = Color(0.075, 0.733, 0.686)
toupe = Color(0.78, 0.675, 0.49)
toxic_green = Color(0.38, 0.871, 0.165)
tree_green = Color(0.165, 0.494, 0.098)
true_blue = Color(0.004, 0.059, 0.8)
true_green = Color(0.031, 0.58, 0.016)
turquoise = Color(0.024, 0.761, 0.675)
turquoise_blue = Color(0.024, 0.694, 0.769)
turquoise_green = Color(0.016, 0.957, 0.537)
turtle_green = Color(0.459, 0.722, 0.31)
twilight = Color(0.306, 0.318, 0.545)
twilight_blue = Color(0.039, 0.263, 0.478)
ugly_blue = Color(0.192, 0.4, 0.541)
ugly_brown = Color(0.49, 0.443, 0.012)
ugly_green = Color(0.478, 0.592, 0.012)
ugly_pink = Color(0.804, 0.459, 0.518)
ugly_purple = Color(0.643, 0.259, 0.627)
ugly_yellow = Color(0.816, 0.757, 0.004)
ultramarine = Color(0.125, 0.0, 0.694)
ultramarine_blue = Color(0.094, 0.02, 0.859)
umber = Color(0.698, 0.392, 0.0)
velvet = Color(0.459, 0.031, 0.318)
vermillion = Color(0.957, 0.196, 0.047)
very_dark_blue = Color(0.0, 0.004, 0.2)
very_dark_brown = Color(0.114, 0.008, 0.0)
very_dark_green = Color(0.024, 0.18, 0.012)
very_dark_purple = Color(0.165, 0.004, 0.204)
very_light_blue = Color(0.835, 1.0, 1.0)
very_light_brown = Color(0.827, 0.714, 0.514)
very_light_green = Color(0.82, 1.0, 0.741)
very_light_pink = Color(1.0, 0.957, 0.949)
very_light_purple = Color(0.965, 0.808, 0.988)
very_pale_blue = Color(0.839, 1.0, 0.996)
very_pale_green = Color(0.812, 0.992, 0.737)
vibrant_blue = Color(0.012, 0.224, 0.973)
vibrant_green = Color(0.039, 0.867, 0.031)
vibrant_purple = Color(0.678, 0.012, 0.871)
violet = Color(0.604, 0.055, 0.918)
violet_blue = Color(0.318, 0.039, 0.788)
violet_pink = Color(0.984, 0.373, 0.988)
violet_red = Color(0.647, 0.0, 0.333)
viridian = Color(0.118, 0.569, 0.404)
vivid_blue = Color(0.082, 0.18, 1.0)
vivid_green = Color(0.184, 0.937, 0.063)
vivid_purple = Color(0.6, 0.0, 0.98)
vomit = Color(0.635, 0.643, 0.082)
vomit_green = Color(0.537, 0.635, 0.012)
vomit_yellow = Color(0.78, 0.757, 0.047)
warm_blue = Color(0.294, 0.341, 0.859)
warm_brown = Color(0.588, 0.306, 0.008)
warm_grey = Color(0.592, 0.541, 0.518)
warm_gray = Color(0.592, 0.541, 0.518)
warm_pink = Color(0.984, 0.333, 0.506)
warm_purple = Color(0.584, 0.18, 0.561)
washed_out_green = Color(0.737, 0.961, 0.651)
water_blue = Color(0.055, 0.529, 0.8)
watermelon = Color(0.992, 0.275, 0.349)
weird_green = Color(0.227, 0.898, 0.498)
wheat = Color(0.984, 0.867, 0.494)
white = Color(1.0, 1.0, 1.0)
windows_blue = Color(0.216, 0.471, 0.749)
wine = Color(0.502, 0.004, 0.247)
wine_red = Color(0.482, 0.012, 0.137)
wintergreen = Color(0.125, 0.976, 0.525)
wisteria = Color(0.659, 0.49, 0.761)
yellow = Color(1.0, 1.0, 0.078)
yellow_brown = Color(0.718, 0.58, 0.0)
yellow_green = Color(0.753, 0.984, 0.176)
yellow_ochre = Color(0.796, 0.616, 0.024)
yellow_orange = Color(0.988, 0.69, 0.004)
yellow_tan = Color(1.0, 0.89, 0.431)
yellow_green = Color(0.784, 0.992, 0.239)
yellowgreen = Color(0.733, 0.976, 0.059)
yellowish = Color(0.98, 0.933, 0.4)
yellowish_brown = Color(0.608, 0.478, 0.004)
yellowish_green = Color(0.69, 0.867, 0.086)
yellowish_orange = Color(1.0, 0.671, 0.059)
yellowish_tan = Color(0.988, 0.988, 0.506)
yellowy_brown = Color(0.682, 0.545, 0.047)
yellowy_green = Color(0.749, 0.945, 0.157)
