yafowil.widget.image
====================

Import requirements::

    >>> import os
    >>> import pkg_resources
    >>> import PIL
    >>> import yafowil.loader
    >>> import yafowil.widget.image
    >>> from StringIO import StringIO
    >>> from yafowil.base import factory

Provide testing dummy files::

    >>> def dummy_file_data(filename):
    ...     path = pkg_resources.resource_filename(
    ...         'yafowil.widget.image', 'testing/%s' % filename)
    ...     with open(path) as file:
    ...         data = file.read()
    ...     return data
    
    >>> dummy_png = dummy_file_data('dummy.png')
    >>> dummy_png
    "\x89PNG\r\n...\x00IEND\xaeB`\x82"
    
    >>> dummy_jpg = dummy_file_data('dummy.jpg')
    >>> dummy_jpg
    '\xff\xd8\xff\xe0\x00\x10JFIF\...\xff\xd9'
    
    >>> dummy_pdf = dummy_file_data('dummy.pdf')
    >>> dummy_pdf
    '%PDF-1.5\n%\...\n956\n%%EOF\n'


Rendering
---------

Empty image::

    >>> form = factory(
    ...     'form',
    ...     name='myform',
    ...     props={'action': 'myaction'})
    >>> form['image'] = factory('image')
    >>> pxml(form())
    <form action="myaction" enctype="multipart/form-data" id="form-myform" method="post" novalidate="novalidate">
      <input accept="image/*" class="image" id="input-myform-image" name="myform.image" type="file"/>
    </form>
    <BLANKLINE>

Image with value. Default file action keep is checked::
    
    >>> form['image'] = factory(
    ...     'image',
    ...     value={
    ...         'file': StringIO(dummy_png),
    ...         'mimetype': 'image/png',
    ...     })
    >>> pxml(form())
    <form action="myaction" enctype="multipart/form-data" id="form-myform" method="post" novalidate="novalidate">
      <input accept="image/*" class="image" id="input-myform-image" name="myform.image" type="file"/>
      <div id="radio-myform-image-keep">
        <input checked="checked" class="image" id="input-myform-image-keep" name="myform.image-action" type="radio" value="keep"/>
        <span>Keep Existing image</span>
      </div>
      <div id="radio-myform-image-replace">
        <input class="image" id="input-myform-image-replace" name="myform.image-action" type="radio" value="replace"/>
        <span>Replace existing image</span>
      </div>
      <div id="radio-myform-image-delete">
        <input class="image" id="input-myform-image-delete" name="myform.image-action" type="radio" value="delete"/>
        <span>Delete existing image</span>
      </div>
    </form>
    <BLANKLINE>

If file URL of existing image is known, ``src`` property can be set do display
image above controls::

    >>> form['image'] = factory(
    ...     'image',
    ...     value={
    ...         'file': StringIO(dummy_png),
    ...         'mimetype': 'image/png',
    ...     },
    ...     props={
    ...         'src': 'http://www.example.com/someimage.png',
    ...         'alt': 'Alternative text',
    ...     })
    >>> pxml(form())
    <form action="myaction" enctype="multipart/form-data" id="form-myform" method="post" novalidate="novalidate">
      <img alt="Alternative text" class="image-preview" id="image-preview-myform-image" src="http://www.example.com/someimage.png?nocache=..."/>
      <input accept="image/*" class="image" id="input-myform-image" name="myform.image" type="file"/>
      <div id="radio-myform-image-keep">
        <input checked="checked" class="image" id="input-myform-image-keep" name="myform.image-action" type="radio" value="keep"/>
        <span>Keep Existing image</span>
      </div>
      <div id="radio-myform-image-replace">
        <input class="image" id="input-myform-image-replace" name="myform.image-action" type="radio" value="replace"/>
        <span>Replace existing image</span>
      </div>
      <div id="radio-myform-image-delete">
        <input class="image" id="input-myform-image-delete" name="myform.image-action" type="radio" value="delete"/>
        <span>Delete existing image</span>
      </div>
    </form>
    <BLANKLINE>

Src property can be callable::

    >>> form['image'].attrs['src'] = lambda w, d: 'http://www.example.com/otherimage.png'
    >>> pxml(form())
    <form action="myaction" enctype="multipart/form-data" id="form-myform" method="post" novalidate="novalidate">
      <img alt="Alternative text" class="image-preview" id="image-preview-myform-image" src="http://www.example.com/otherimage.png?nocache=..."/>
      <input accept="image/*" class="image" id="input-myform-image" name="myform.image" type="file"/>
      <div id="radio-myform-image-keep">
        <input checked="checked" class="image" id="input-myform-image-keep" name="myform.image-action" type="radio" value="keep"/>
        <span>Keep Existing image</span>
      </div>
      <div id="radio-myform-image-replace">
        <input class="image" id="input-myform-image-replace" name="myform.image-action" type="radio" value="replace"/>
        <span>Replace existing image</span>
      </div>
      <div id="radio-myform-image-delete">
        <input class="image" id="input-myform-image-delete" name="myform.image-action" type="radio" value="delete"/>
        <span>Delete existing image</span>
      </div>
    </form>
    <BLANKLINE>

Render in display mode::

    >>> form['image'].mode = 'display'
    >>> pxml(form())
    <form action="myaction" enctype="multipart/form-data" id="form-myform" method="post" novalidate="novalidate">
      <img alt="Alternative text" src="http://www.example.com/otherimage.png"/>
    </form>
    <BLANKLINE>
    
    >>> form['image'].attrs['src'] = None
    
    >>> pxml(form())
    <form action="myaction" enctype="multipart/form-data" id="form-myform" method="post" novalidate="novalidate"/>
    <BLANKLINE>
    
    >>> form['image'].attrs['src'] = 'http://www.example.com/someimage.png'
    
    >>> form['image'].mode = 'edit'


Base Extraction
---------------

Extract empty (submitted but no upload)::

    >>> request = {}
    >>> data = form.extract(request)
    >>> data['image'].extracted

Extract ``new``::

    >>> request = {
    ...     'myform.image': {
    ...         'file': StringIO(dummy_png),
    ...         'mimetype': 'image/png',
    ...     },
    ... }
    >>> data = form.extract(request)
    >>> data['image'].extracted
    {'mimetype': 'image/png', 
    'action': 'new', 
    'image': <PIL.PngImagePlugin.PngImageFile image mode=RGBA size=50x50 at ...>, 
    'file': <StringIO.StringIO instance at ...>}
    
    >>> data['image'].errors
    []

Extract ``keep`` returns original value::
    
    >>> request = {
    ...     'myform.image': {
    ...         'file': StringIO(dummy_jpg),
    ...         'mimetype': 'image/jpg',
    ...     },
    ...     'myform.image-action': 'keep',
    ... }
    >>> data = form.extract(request)  
    >>> data['image'].extracted
    {'mimetype': 'image/png', 
    'action': 'keep', 
    'image': <PIL.PngImagePlugin.PngImageFile image mode=RGBA size=50x50 at ...>, 
    'file': <StringIO.StringIO instance at ...>}
    
    >>> data['image'].errors
    []

    >>> data['image'].extracted['file'].read()
    "\x89PNG\r\n\...\x00IEND\xaeB`\x82"

Extract ``replace`` returns new value::

    >>> request['myform.image-action'] = 'replace'
    >>> data = form.extract(request)
    >>> data['image'].value
    {'mimetype': 'image/png', 
    'action': 'replace', 
    'image': <PIL.PngImagePlugin.PngImageFile image mode=RGBA size=50x50 at ...>, 
    'file': <StringIO.StringIO instance at ...>}
    
    >>> data['image'].extracted
    {'mimetype': 'image/jpg', 
    'action': 'replace', 
    'image': <PIL.JpegImagePlugin.JpegImageFile image mode=RGB size=50x50 at ...>, 
    'file': <StringIO.StringIO instance at ...>}
    
    >>> data['image'].extracted['file'].read()
    '\xff\xd8\xff\xe0\x00\x10JFIF\...\xff\xd9'
    
    >>> data['image'].errors
    []

Extract ``delete`` returns UNSET::

    >>> request['myform.image-action'] = 'delete'
    >>> data = form.extract(request)
    >>> data['image'].extracted
    {'mimetype': 'image/png', 
    'action': 'delete', 
    'image': <PIL.PngImagePlugin.PngImageFile image mode=RGBA size=50x50 at ...>, 
    'file': <UNSET>}
    
    >>> data['image'].errors
    []


Mimetype extraction
-------------------

Image ``accept`` might be undefined::

    >>> form['image'] = factory(
    ...     'image',
    ...     props={
    ...         'accept': ''
    ...     }
    ... )
    >>> request = {
    ...     'myform.image': {
    ...         'file': StringIO(dummy_jpg),
    ...         'mimetype': 'image/jpg',
    ...     },
    ... }
    >>> form.extract(request)
    <RuntimeData myform, value=<UNSET>, 
    extracted=odict([('image', 
    {'mimetype': 'image/jpg', 
    'action': 'new', 
    'image': <PIL.JpegImagePlugin.JpegImageFile image mode=RGB size=50x50 at ...>, 
    'file': <StringIO.StringIO instance at ...>})]) at ...>

or must be of type ``image``::

    >>> form['image'] = factory(
    ...     'image',
    ...     props={
    ...         'accept': 'text/*'
    ...     }
    ... )
    >>> request = {
    ...     'myform.image': {
    ...         'file': StringIO(dummy_jpg),
    ...         'mimetype': 'image/jpg',
    ...     },
    ... }
    >>> data = form.extract(request)
    Traceback (most recent call last):
      ...
    ValueError: Incompatible mimetype text/*

Explicit image type::

    >>> form['image'] = factory(
    ...     'image',
    ...     props={
    ...         'accept': 'image/png'
    ...     }
    ... )
    >>> data = form.extract(request)
    >>> data['image'].errors
    [ExtractionError('Uploaded image not of type png',)]
    
    >>> form['image'] = factory(
    ...     'image',
    ...     props={
    ...         'accept': 'image/jpg'
    ...     }
    ... )
    >>> form.extract(request)
    <RuntimeData myform, value=<UNSET>, extracted=odict([('image', 
    {'mimetype': 'image/jpg', 
    'action': 'new', 
    'image': <PIL.JpegImagePlugin.JpegImageFile image mode=RGB size=50x50 at ...>, 
    'file': <StringIO.StringIO instance at ...>})]) at ...>

Uploded file not an image::

    >>> request = {
    ...     'myform.image': {
    ...         'file': StringIO(dummy_pdf),
    ...         'mimetype': 'application/pdf',
    ...     },
    ... }
    >>> data = form.extract(request)
    >>> data['image'].errors
    [ExtractionError('Uploaded file is not an image.',)]


Size extraction
---------------

::
    >>> buffer = StringIO(dummy_png)
    >>> image = PIL.Image.open(buffer)
    >>> image
    <PIL.PngImagePlugin.PngImageFile image mode=RGBA size=50x50 at ...>
    
    >>> buffer.seek(0)
    >>> buffer.read()
    "\x89PNG\r\n...\x00IEND\xaeB`\x82"
    
    >>> image.size
    (50, 50)

Minsize::

    >>> form['image'] = factory(
    ...     'image',
    ...     props={
    ...         'minsize': (60, 60),
    ...     }
    ... )
    >>> request = {
    ...     'myform.image': {
    ...         'file': StringIO(dummy_png),
    ...         'mimetype': 'image/png',
    ...     },
    ... }
    >>> data = form.extract(request)
    >>> data['image'].errors
    [ExtractionError('Image must have a minimum size of 60 x 60 pixel',)]
    
    >>> form['image'] = factory(
    ...     'image',
    ...     props={
    ...         'minsize': (40, 40),
    ...     }
    ... )
    >>> data = form.extract(request)
    >>> data['image'].errors
    []

Maxsize::

    >>> form['image'] = factory(
    ...     'image',
    ...     props={
    ...         'maxsize': (40, 40),
    ...     }
    ... )
    >>> data = form.extract(request)
    >>> data['image'].errors
    [ExtractionError('Image must have a maximum size of 40 x 40 pixel',)]
    
    >>> form['image'] = factory(
    ...     'image',
    ...     props={
    ...         'maxsize': (60, 60),
    ...     }
    ... )
    >>> data = form.extract(request)
    >>> data['image'].errors
    []

Exact size::

    >>> form['image'] = factory(
    ...     'image',
    ...     props={
    ...         'minsize': (40, 40),
    ...         'maxsize': (40, 40),
    ...     }
    ... )
    >>> data = form.extract(request)
    >>> data['image'].errors
    [ExtractionError('Image must have a size of 40 x 40 pixel',)]
    
    >>> form['image'] = factory(
    ...     'image',
    ...     props={
    ...         'minsize': (50, 50),
    ...         'maxsize': (50, 50),
    ...     }
    ... )
    >>> data = form.extract(request)
    >>> data['image'].errors
    []


DPI extraction
--------------

::
    >>> image.info['dpi']
    (72, 72)

Minimum DPI::

    >>> form['image'] = factory(
    ...     'image',
    ...     props={
    ...         'mindpi': (80, 80),
    ...     }
    ... )
    >>> request = {
    ...     'myform.image': {
    ...         'file': StringIO(dummy_png),
    ...         'mimetype': 'image/png',
    ...     },
    ... }
    >>> data = form.extract(request)
    >>> data['image'].errors
    [ExtractionError('Image must have at least 80 x 80 DPI',)]
    
    >>> form['image'] = factory(
    ...     'image',
    ...     props={
    ...         'mindpi': (60, 60),
    ...     }
    ... )
    >>> data = form.extract(request)
    >>> data['image'].errors
    []

Maximum DPI::

    >>> form['image'] = factory(
    ...     'image',
    ...     props={
    ...         'maxdpi': (60, 60),
    ...     }
    ... )
    >>> request = {
    ...     'myform.image': {
    ...         'file': StringIO(dummy_png),
    ...         'mimetype': 'image/png',
    ...     },
    ... }
    >>> data = form.extract(request)
    >>> data['image'].errors
    [ExtractionError('Image must have a maximum of 60 x 60 DPI',)]
    
    >>> form['image'] = factory(
    ...     'image',
    ...     props={
    ...         'maxdpi': (80, 80),
    ...     }
    ... )
    >>> data = form.extract(request)
    >>> data['image'].errors
    []

Exact DPI::

    >>> form['image'] = factory(
    ...     'image',
    ...     props={
    ...         'mindpi': (60, 60),
    ...         'maxdpi': (60, 60),
    ...     }
    ... )
    >>> request = {
    ...     'myform.image': {
    ...         'file': StringIO(dummy_png),
    ...         'mimetype': 'image/png',
    ...     },
    ... }
    >>> data = form.extract(request)
    >>> data['image'].errors
    [ExtractionError('Image must have a resolution of 60 x 60 DPI',)]
    
    >>> form['image'] = factory(
    ...     'image',
    ...     props={
    ...         'mindpi': (72, 72),
    ...         'maxdpi': (72, 72),
    ...     }
    ... )
    >>> data = form.extract(request)
    >>> data['image'].errors
    []


Scales Extraction
-----------------

::
    >>> form['image'] = factory(
    ...     'image',
    ...     props={
    ...         'scales': {
    ...             'micro': (20, 20),
    ...             'landscape': (70, 40),
    ...             'portrait': (40, 70),
    ...         },
    ...     }
    ... )
    >>> request = {
    ...     'myform.image': {
    ...         'file': StringIO(dummy_png),
    ...         'mimetype': 'image/png',
    ...     },
    ... }
    >>> data = form.extract(request)
    >>> extracted = data['image'].extracted
    >>> extracted
    {'mimetype': 'image/png', 
    'action': 'new', 
    'image': <PIL.PngImagePlugin.PngImageFile image mode=RGBA size=50x50 at ...>, 
    'file': <StringIO.StringIO instance at ...>, 
    'scales': 
    {'micro': <PIL.Image.Image image mode=RGBA size=20x20 at ...>, 
    'landscape': <PIL.Image.Image image mode=RGBA size=40x40 at ...>, 
    'portrait': <PIL.Image.Image image mode=RGBA size=40x40 at ...>}}
    
    >>> for name, image in extracted['scales'].items():
    ...     path = pkg_resources.resource_filename(
    ...         'yafowil.widget.image', 'testing/%s.png' % name)
    ...     image.save(path, quality=100)


Cropping Extraction
-------------------

Cropping logic::

    >>> left, top, width, height = 7, 3, 30, 40
    >>> cropped = image.crop((left, top, width, height))
    >>> path = pkg_resources.resource_filename(
    ...     'yafowil.widget.image', 'testing/cropped.png')
    >>> cropped.save(path, quality=100)

Fitting logic::

    >>> from imageutils.size import (
    ...     same_aspect_ratio,
    ...     aspect_ratio_approximate,
    ...     scale_size,
    ... )
    >>> same_aspect_ratio((300, 200), (600, 400))
    True

scale X down::

    >>> scale_size((100, 50), (75, None))
    (75, 37)
    
scale X up::

    >>> scale_size((100, 50), (150, None))
    (150, 75)
    
scale Y down::

    >>> scale_size((100, 50), (None, 25))
    (50, 25)
    
scale Y up::

    >>> scale_size((100, 50), (None, 100))
    (200, 100)

scale x::

    >>> size_from = (60, 40)
    >>> size_to = (50, 25)
    >>> aspect_ratio_approximate(size_from)
    Decimal('1.50')
    
    >>> aspect_ratio_approximate(size_to)
    Decimal('2.00')
    
    >>> aspect_ratio_approximate(size_from) < aspect_ratio_approximate(size_to)
    True
    
    >>> scaled = scale_size(size_from, (size_to[0], None))
    >>> scaled
    (50, 33)
    
    >>> offset_y = (scaled[1] - size_to[1]) / 2
    >>> offset_y
    4

scale y::

    >>> size_from = (60, 40)
    >>> size_to = (50, 35)
    >>> aspect_ratio_approximate(size_from)
    Decimal('1.50')
    
    >>> aspect_ratio_approximate(size_to)
    Decimal('1.43')

    >>> aspect_ratio_approximate(size_from) > aspect_ratio_approximate(size_to)
    True
    
    >>> scaled = scale_size(size_from, (None, size_to[1]))
    >>> scaled
    (52, 35)
    
    >>> offset_x = (scaled[0] - size_to[0]) / 2
    >>> offset_x
    1

Crop as is without offset, size (20, 20)::

    >>> form['image'] = factory(
    ...     'image',
    ...     props={
    ...         'crop': {
    ...             'size': (20, 20),
    ...         },
    ...     }
    ... )
    >>> request = {
    ...     'myform.image': {
    ...         'file': StringIO(dummy_png),
    ...         'mimetype': 'image/png',
    ...     },
    ... }
    >>> data = form.extract(request)
    >>> extracted = data['image'].extracted
    >>> extracted
    {'mimetype': 'image/png', 
    'action': 'new', 
    'image': <PIL.PngImagePlugin.PngImageFile image mode=RGBA size=50x50 at ...>, 
    'cropped': <PIL.Image._ImageCrop image mode=RGBA size=20x20 at ...>, 
    'file': <StringIO.StringIO instance at ...>}
    
    >>> path = pkg_resources.resource_filename(
    ...     'yafowil.widget.image', 'testing/crop_size_20_20.png')
    >>> extracted['cropped'].save(path, quality=100)

Crop as is without offset, size (40, 20)::

    >>> form['image'] = factory(
    ...     'image',
    ...     props={
    ...         'crop': {
    ...             'size': (40, 20),
    ...         },
    ...     }
    ... )
    >>> request = {
    ...     'myform.image': {
    ...         'file': StringIO(dummy_png),
    ...         'mimetype': 'image/png',
    ...     },
    ... }
    >>> data = form.extract(request)
    >>> extracted = data['image'].extracted
    >>> extracted
    {'mimetype': 'image/png', 
    'action': 'new', 
    'image': <PIL.PngImagePlugin.PngImageFile image mode=RGBA size=50x50 at ...>, 
    'cropped': <PIL.Image._ImageCrop image mode=RGBA size=40x20 at ...>, 
    'file': <StringIO.StringIO instance at ...>}
    
    >>> path = pkg_resources.resource_filename(
    ...     'yafowil.widget.image', 'testing/crop_size_40_20.png')
    >>> extracted['cropped'].save(path, quality=100)

Crop as is without offset, size (20, 40)::

    >>> form['image'] = factory(
    ...     'image',
    ...     props={
    ...         'crop': {
    ...             'size': (20, 40),
    ...         },
    ...     }
    ... )
    >>> request = {
    ...     'myform.image': {
    ...         'file': StringIO(dummy_png),
    ...         'mimetype': 'image/png',
    ...     },
    ... }
    >>> data = form.extract(request)
    >>> extracted = data['image'].extracted
    >>> extracted
    {'mimetype': 'image/png', 
    'action': 'new', 
    'image': <PIL.PngImagePlugin.PngImageFile image mode=RGBA size=50x50 at ...>, 
    'cropped': <PIL.Image._ImageCrop image mode=RGBA size=20x40 at ...>, 
    'file': <StringIO.StringIO instance at ...>}
    
    >>> path = pkg_resources.resource_filename(
    ...     'yafowil.widget.image', 'testing/crop_size_20_40.png')
    >>> extracted['cropped'].save(path, quality=100)

Crop with offset (5, 3), size (20, 40)::

    >>> form['image'] = factory(
    ...     'image',
    ...     props={
    ...         'crop': {
    ...             'size': (20, 40),
    ...             'offset': (5, 3),
    ...         },
    ...     }
    ... )
    >>> request = {
    ...     'myform.image': {
    ...         'file': StringIO(dummy_png),
    ...         'mimetype': 'image/png',
    ...     },
    ... }
    >>> data = form.extract(request)
    >>> extracted = data['image'].extracted
    >>> extracted
    {'mimetype': 'image/png', 
    'action': 'new', 
    'image': <PIL.PngImagePlugin.PngImageFile image mode=RGBA size=50x50 at ...>, 
    'cropped': <PIL.Image._ImageCrop image mode=RGBA size=20x40 at ...>, 
    'file': <StringIO.StringIO instance at ...>}
    
    >>> path = pkg_resources.resource_filename(
    ...     'yafowil.widget.image', 'testing/crop_size_20_40_offset_5_3.png')
    >>> extracted['cropped'].save(path, quality=100)

Crop with offset (5, 0), size (50, 20) -> x overflow::

    >>> form['image'] = factory(
    ...     'image',
    ...     props={
    ...         'crop': {
    ...             'size': (50, 20),
    ...             'offset': (5, 0),
    ...         },
    ...     }
    ... )
    >>> request = {
    ...     'myform.image': {
    ...         'file': StringIO(dummy_png),
    ...         'mimetype': 'image/png',
    ...     },
    ... }
    >>> data = form.extract(request)
    >>> extracted = data['image'].extracted
    >>> extracted
    {'mimetype': 'image/png', 
    'action': 'new', 
    'image': <PIL.PngImagePlugin.PngImageFile image mode=RGBA size=50x50 at ...>, 
    'cropped': <PIL.Image._ImageCrop image mode=RGBA size=50x20 at ...>, 
    'file': <StringIO.StringIO instance at ...>}
    
    >>> path = pkg_resources.resource_filename(
    ...     'yafowil.widget.image', 'testing/crop_size_50_20_offset_5_0.png')
    >>> extracted['cropped'].save(path, quality=100)

Crop fitting::

    >>> dummy_40_20_png = dummy_file_data('crop_size_40_20.png')
    >>> dummy_40_20_png
    '\x89PNG\r\n\...\x00IEND\xaeB`\x82'
    
    >>> dummy_20_40_png = dummy_file_data('crop_size_20_40.png')
    >>> dummy_20_40_png
    '\x89PNG\r\n\...\x00IEND\xaeB`\x82'

Crop fitting from lanscape, size (30, 18)::

    >>> form['image'] = factory(
    ...     'image',
    ...     props={
    ...         'crop': {
    ...             'size': (30, 18),
    ...             'fitting': True,
    ...         },
    ...     }
    ... )
    >>> request = {
    ...     'myform.image': {
    ...         'file': StringIO(dummy_40_20_png),
    ...         'mimetype': 'image/png',
    ...     },
    ... }
    >>> data = form.extract(request)
    >>> extracted = data['image'].extracted
    >>> extracted
    {'mimetype': 'image/png', 
    'action': 'new', 
    'image': <PIL.PngImagePlugin.PngImageFile image mode=RGBA size=40x20 at ...>, 
    'cropped': <PIL.Image._ImageCrop image mode=RGBA size=30x18 at ...>, 
    'file': <StringIO.StringIO instance at ...>}
    
    >>> path = pkg_resources.resource_filename(
    ...     'yafowil.widget.image', 'testing/crop_fitting_ls_30_18.png')
    >>> extracted['cropped'].save(path, quality=100)

Crop fitting from landscape, size (18, 30)::

    >>> form['image'] = factory(
    ...     'image',
    ...     props={
    ...         'crop': {
    ...             'size': (18, 30),
    ...             'fitting': True,
    ...         },
    ...     }
    ... )
    >>> request = {
    ...     'myform.image': {
    ...         'file': StringIO(dummy_40_20_png),
    ...         'mimetype': 'image/png',
    ...     },
    ... }
    >>> data = form.extract(request)
    >>> extracted = data['image'].extracted
    >>> extracted
    {'mimetype': 'image/png', 
    'action': 'new', 
    'image': <PIL.PngImagePlugin.PngImageFile image mode=RGBA size=40x20 at ...>, 
    'cropped': <PIL.Image._ImageCrop image mode=RGBA size=18x30 at ...>, 
    'file': <StringIO.StringIO instance at ...>}
    
    >>> path = pkg_resources.resource_filename(
    ...     'yafowil.widget.image', 'testing/crop_fitting_ls_18_30.png')
    >>> extracted['cropped'].save(path, quality=100)

Crop fitting from portrait, size (30, 18)::

    >>> form['image'] = factory(
    ...     'image',
    ...     props={
    ...         'crop': {
    ...             'size': (30, 18),
    ...             'fitting': True,
    ...         },
    ...     }
    ... )
    >>> request = {
    ...     'myform.image': {
    ...         'file': StringIO(dummy_20_40_png),
    ...         'mimetype': 'image/png',
    ...     },
    ... }
    >>> data = form.extract(request)
    >>> extracted = data['image'].extracted
    >>> extracted
    {'mimetype': 'image/png', 
    'action': 'new', 
    'image': <PIL.PngImagePlugin.PngImageFile image mode=RGBA size=20x40 at ...>, 
    'cropped': <PIL.Image._ImageCrop image mode=RGBA size=30x18 at ...>, 
    'file': <StringIO.StringIO instance at ...>}
    
    >>> path = pkg_resources.resource_filename(
    ...     'yafowil.widget.image', 'testing/crop_fitting_pt_30_18.png')
    >>> extracted['cropped'].save(path, quality=100)

Crop fitting from portrait, size (18, 30)::

    >>> form['image'] = factory(
    ...     'image',
    ...     props={
    ...         'crop': {
    ...             'size': (18, 30),
    ...             'fitting': True,
    ...         },
    ...     }
    ... )
    >>> request = {
    ...     'myform.image': {
    ...         'file': StringIO(dummy_20_40_png),
    ...         'mimetype': 'image/png',
    ...     },
    ... }
    >>> data = form.extract(request)
    >>> extracted = data['image'].extracted
    >>> extracted
    {'mimetype': 'image/png', 
    'action': 'new', 
    'image': <PIL.PngImagePlugin.PngImageFile image mode=RGBA size=20x40 at ...>, 
    'cropped': <PIL.Image._ImageCrop image mode=RGBA size=18x30 at ...>, 
    'file': <StringIO.StringIO instance at ...>}
    
    >>> path = pkg_resources.resource_filename(
    ...     'yafowil.widget.image', 'testing/crop_fitting_pt_18_30.png')
    >>> extracted['cropped'].save(path, quality=100)

Crop fitting square -> thus also same ratio::

    >>> form['image'] = factory(
    ...     'image',
    ...     props={
    ...         'crop': {
    ...             'size': (30, 30),
    ...             'fitting': True,
    ...         },
    ...     }
    ... )
    >>> request = {
    ...     'myform.image': {
    ...         'file': StringIO(dummy_png),
    ...         'mimetype': 'image/png',
    ...     },
    ... }
    >>> data = form.extract(request)
    >>> extracted = data['image'].extracted
    >>> extracted
    {'mimetype': 'image/png', 
    'action': 'new', 
    'image': <PIL.PngImagePlugin.PngImageFile image mode=RGBA size=50x50 at ...>, 
    'cropped': <PIL.Image._ImageCrop image mode=RGBA size=30x30 at ...>, 
    'file': <StringIO.StringIO instance at ...>}
    
    >>> path = pkg_resources.resource_filename(
    ...     'yafowil.widget.image', 'testing/crop_fitting_sq_30_30.png')
    >>> extracted['cropped'].save(path, quality=100)

Crop fitting portrait from square::

    >>> form['image'] = factory(
    ...     'image',
    ...     props={
    ...         'crop': {
    ...             'size': (40, 50),
    ...             'fitting': True,
    ...         },
    ...     }
    ... )
    >>> request = {
    ...     'myform.image': {
    ...         'file': StringIO(dummy_png),
    ...         'mimetype': 'image/png',
    ...     },
    ... }
    >>> data = form.extract(request)
    >>> extracted = data['image'].extracted
    >>> extracted
    {'mimetype': 'image/png', 
    'action': 'new', 
    'image': <PIL.PngImagePlugin.PngImageFile image mode=RGBA size=50x50 at ...>, 
    'cropped': <PIL.Image._ImageCrop image mode=RGBA size=40x50 at ...>, 
    'file': <StringIO.StringIO instance at ...>}
    
    >>> path = pkg_resources.resource_filename(
    ...     'yafowil.widget.image', 'testing/crop_fitting_sq_40_50.png')
    >>> extracted['cropped'].save(path, quality=100)

Crop fitting lanscape from square::

    >>> form['image'] = factory(
    ...     'image',
    ...     props={
    ...         'crop': {
    ...             'size': (48, 40),
    ...             'fitting': True,
    ...         },
    ...     }
    ... )
    >>> request = {
    ...     'myform.image': {
    ...         'file': StringIO(dummy_png),
    ...         'mimetype': 'image/png',
    ...     },
    ... }
    >>> data = form.extract(request)
    >>> extracted = data['image'].extracted
    >>> extracted
    {'mimetype': 'image/png', 
    'action': 'new', 
    'image': <PIL.PngImagePlugin.PngImageFile image mode=RGBA size=50x50 at ...>, 
    'cropped': <PIL.Image._ImageCrop image mode=RGBA size=48x40 at ...>, 
    'file': <StringIO.StringIO instance at ...>}
    
    >>> path = pkg_resources.resource_filename(
    ...     'yafowil.widget.image', 'testing/crop_fitting_sq_48_40.png')
    >>> extracted['cropped'].save(path, quality=100)


Saving data
-----------

Save either by filename or file descriptor::

    >>> buffer = StringIO(dummy_png)
    >>> image = PIL.Image.open(buffer)
    >>> out = StringIO()
    >>> image.save(out, 'png', quality=100)
    >>> out.seek(0)
    >>> out.read()
    "\x89PNG\r\n\...\x00IEND\xaeB`\x82"
    