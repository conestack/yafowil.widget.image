Changes
=======

1.6 (2022-10-06)
----------------

- Introduce ``rounddpi`` flag for image blueprint. Pillow, as of version 6.0,
  no longer rounds reported DPI values for BMP, JPEG and PNG images, but image
  manipulation programs may not produce accurate DPI values.
  [rnix]


1.5 (2018-07-16)
----------------

- Python 3 compatibility.
  [rnix]

- Convert doctests to unittests.
  [rnix]


1.4.1 (2017-03-01)
------------------

- Create runtime images directory for example only if examples are really used.
  [rnix, 2017-08-24]


1.4 (2017-03-01)
----------------

- Use ``yafowil.utils.entry_point`` decorator.
  [rnix, 2016-06-28]

- Copy over used functions from ``ImageUtils`` package and drop dependency.
  [rnix, 2016-06-28]

- Use ``&amp;`` instead of ``&`` for parameter separation in
  ``image_edit_renderer`` if image URL already contains GET parameters.
  [rnix, 2015-10-05]


1.3 (2015-01-23)
----------------

- Add top margin to input.
  [rnix, 2014-08-06]

- Check for already existing query parameters befor adding nocache param to
  img src.
  [rnix, 2014-07-11]


1.2
---

- Add translations, package depends now ``yafowil`` >= 2.1
  [rnix, 2014-04-30]


1.1.2
-----

- CSS fix.
  [rnix, 2012-10-30]


1.1.1
-----

- use ``yafowil.utils.attr_value`` wherever possible.
  [rnix, 2012-10-25]


1.1
---

- Adopt resource providing
  [rnix, 2012-06-12]

- Provide example widget
  [rnix, 2012-06-12]


1.0.1
-----

- Add ``nocache`` request parameter to image ``src`` on edit.
  [rnix, 2012-31-05]

- JS Fix.
  [rnix, 2012-31-05]


1.0
---

- Make it work
  [rnix]
