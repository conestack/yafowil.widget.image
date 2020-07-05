# borrowed from https://pypi.python.org/pypi/ImageUtils
from decimal import Decimal


def aspect_ratio_approximate(size):
    """Gets a decimal approximation of an aspect ratio.
    """
    return Decimal('%.2f' % (float(size[0]) / size[1]))


def same_aspect_ratio(size1, size2):
    """Determines if two sizes have the same aspect ratio.
    """
    return aspect_ratio_approximate(size1) == aspect_ratio_approximate(size2)


def scale_size(size, sizer):
    """Scales a size tuple based on a sizer tuple.

    A sizer is just a size tuple that specifies only width or height.
    """
    if not any(sizer):
        return size
    size_new = list(sizer)
    i = size_new.index(None)
    j = i * -1 + 1
    size_new[i] = (size_new[j] * size[i]) // size[j]
    return tuple(size_new)
