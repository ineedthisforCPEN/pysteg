"""dimensions.py
"""


import math
import re


__RE_RATIO = re.compile(r"^\d+(?::\d+)*$")


def __get_ratios(rstring):
    """Convert a given ratio string (numbers separated by colons) into
    an integer tuple.

    Parameters:
        rstring     Ratio string to convert to tuple

    Return:
        Returns the converted tuple.

    Raises:
        SyntaxError

    Example:
        __get_ratios("1") -> (1,)
        __get_ratios("1:2") -> (1, 2,)
        __get_ratios("1:2:3") -> (1, 2, 3,)

        __get_ratios("1:2:") -> SyntaxError
        __get_ratios("1::2") -> SyntaxError
        __get_ratios("a:b:c") -> SyntaxError
    """
    if __RE_RATIO.match(rstring) is None:
        raise SyntaxError(f"Invalid ratio string '{rstring}'")

    return tuple(int(i) for i in rstring.split(":"))


def ndims(volume, rstring):
    """Find an n-dimensional vector such that their product is
    optimized to be the smallest volume that contains the given volume
    and maintains the given ratio.

    Parameters:
        volume      Volume for which to optimize
        rstring     Ratio of dimensions for optimized volume as string

    Return:
        Returns n-sized tuple where each element is the width of the
        volume along that dimension. The product of these elements is
        guaranteed to be greater than or equal to 'volume'.

    Note:
        If the product of the initial ratio is larger than the initial
        volume, the return value will be identical to the ratios.

    Example:
        ndims(8, "1") -> (8)
        ndims(8, "3") -> (9)
        ndims(8, "9") -> (9)

        ndims(8, "1:2") -> (2, 4)
        ndims(8, "1:8") -> (1, 8)
        ndims(7, "1:2") -> (2, 4)

        ndims(8, "1:1:1") -> (2, 2, 2)
        ndims(8, "1:2:4") -> (1, 2, 4)
        ndims(7, "1:1:1") -> (2, 2, 2)
    """
    ratios = __get_ratios(rstring)
    n = len(ratios)
    p = math.prod(ratios)
    i = math.ceil((volume / p) ** (1 / n))

    return tuple(r*i for r in ratios)
