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
    '\x89PNG\r\n...\x00IEND\xaeB`\x82'
    
    >>> dummy_jpg = dummy_file_data('dummy.jpg')
    >>> dummy_jpg
    '\xff\xd8\xff\xe0\x00\x10JFIF\...?\xff\xd9'
    
    >>> dummy_pdf = dummy_file_data('dummy.pdf')
    >>> dummy_pdf
    '%PDF-1.5\n%\...\n956\n%%EOF\n'

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
    '\x89PNG\r\n\...\x00IEND\xaeB`\x82'

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
    '\xff\xd8\xff\xe0\x00\x10JFIF\...?\xff\xd9'
    
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

If file URL of existing image is known, ``src`` property can be set do display
image above controls::

    >>> form['image'] = factory(
    ...     'image',
    ...     value={'file': StringIO(dummy_png)},
    ...     props={
    ...         'src': 'http://www.example.com/someimage.png',
    ...         'alt': 'Alternative text',
    ...     })
    >>> pxml(form())
    <form action="myaction" enctype="multipart/form-data" id="form-myform" method="post" novalidate="novalidate">
      <img alt="Alternative text" class="image-preview" id="image-preview-myform-image" src="http://www.example.com/someimage.png"/>
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

Mimetype extraction.

Image ``accept`` must be of type ``image``::

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

Size extraction::

    >>> buffer = StringIO(dummy_png)
    >>> image = PIL.Image.open(buffer)
    >>> image
    <PIL.PngImagePlugin.PngImageFile image mode=RGBA size=50x50 at ...>
    
    >>> buffer.seek(0)
    >>> buffer.read()
    '\x89PNG\r\n...\x00IEND\xaeB`\x82'
    
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

DPI extraction::

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
