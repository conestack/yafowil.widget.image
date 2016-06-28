image utils
===========

Imports::

    >>> from yafowil.widget.image.utils import aspect_ratio_approximate
    >>> from yafowil.widget.image.utils import same_aspect_ratio
    >>> from yafowil.widget.image.utils import scale_size

aspect ratio approximate::

    >>> aspect_ratio_approximate((640, 480))
    Decimal('1.33')

    >>> aspect_ratio_approximate((4, 3))
    Decimal('1.33')

same aspect ratio::

    >>> same_aspect_ratio((640, 480), (4, 3))
    True

    >>> same_aspect_ratio((1280, 1024), (4, 3))
    False

scale size::

    >>> scale_size((640, 480), (800, None))
    (800, 600)

    >>> scale_size((640, 480), (None, 3))
    (4, 3)
