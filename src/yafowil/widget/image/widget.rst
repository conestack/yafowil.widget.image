Import requirements::

    >>> import os
    >>> import pkg_resources
    >>> import PIL
    >>> import yafowil.loader
    >>> import yafowil.widget.image
    >>> from StringIO import StringIO
    >>> from yafowil.base import factory

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

    >>> image_path = pkg_resources.resource_filename(
    ...     'yafowil.widget.image', 'testing/dummy.png')
    
    >>> os.path.exists(image_path)
    True
    
    >>> with open(image_path) as dummy_image:
    ...     value = dummy_image.read()
    
    >>> value
    '\x89PNG\r\n...\x00IEND\xaeB`\x82'
    
    >>> form['image'] = factory('image', value={'file': StringIO(value)})
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
    ...     'myform.image': {'file': StringIO('123')},
    ... }
    >>> data = form.extract(request)    
    >>> data.printtree()
    <RuntimeData myform, value=<UNSET>, extracted=odict([('image', {'action': 'new', 'file': <StringIO.StringIO instance at ...>})]) at ...>
      <RuntimeData myform.image, value={'file': <StringIO.StringIO instance at ...>}, extracted={'action': 'new', 'file': <StringIO.StringIO instance at ...>} at ...>

Extract ``keep`` returns original value::
    
    >>> request = {
    ...     'myform.image': {'file': StringIO('123')},
    ...     'myform.image-action': 'keep'
    ... }
    >>> data = form.extract(request)    
    >>> data.printtree()
    <RuntimeData myform, value=<UNSET>, extracted=odict([('image', {'action': 'keep', 'file': <StringIO.StringIO instance at ...>})]) at ...>
      <RuntimeData myform.image, value={'action': 'keep', 'file': <StringIO.StringIO instance at ...>}, extracted={'action': 'keep', 'file': <StringIO.StringIO instance at ...>} at ...>

    >>> data['image'].extracted['file'].read()
    '\x89PNG\r\n\...\x00IEND\xaeB`\x82'
    
    >>> data['image'].extracted['action']
    'keep'

Extract ``replace`` returns new value::

    >>> request['myform.image-action'] = 'replace'
    >>> data = form.extract(request)
    >>> data.extracted
    odict([('image', {'action': 'replace', 'file': <StringIO.StringIO instance at ...>})])
    
    >>> data['image'].extracted['file'].read()
    '123'
    
    >>> data['image'].extracted['action']
    'replace'

Extract ``delete`` returns UNSET::

    >>> request['myform.image-action'] = 'delete'
    >>> data = form.extract(request)
    >>> data.extracted
    odict([('image', {'action': 'delete', 'file': <UNSET>})])
    
    >>> data['image'].extracted['action']
    'delete'

If file URL of existing image is known, ``src`` property can be set do display
image above controls::

    >>> form['image'] = factory(
    ...     'image',
    ...     value=value,
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
