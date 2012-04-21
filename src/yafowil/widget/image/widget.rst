Import requirements::

    >>> import os
    >>> import pkg_resources
    >>> import PIL
    >>> import yafowil.loader
    >>> import yafowil.widget.image
    >>> from yafowil.base import factory

Empty image::

    >>> form = factory(
    ...     'form',
    ...     name='myform',
    ...     props={'action': 'myaction'})
    >>> form['image'] = factory('image', 'myimage')
    >>> pxml(form())
    <form action="myaction" enctype="multipart/form-data" id="form-myform" method="post" novalidate="novalidate">
      <input accept="image/*" class="image" id="input-myform-image" name="myform.image" type="file"/>
    </form>
    <BLANKLINE>

Image with value::

    >>> image_path = pkg_resources.resource_filename(
    ...     'yafowil.widget.image', 'testing/dummy.png')
    
    >>> os.path.exists(image_path)
    True
    
    >>> with open(image_path) as dummy_image:
    ...     value = dummy_image.read()
    
    >>> value
    '\x89PNG\r\n...\x00IEND\xaeB`\x82'
    
    >>> form['image'] = factory('image', 'myimage', value=value)
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
    
    >>> request = {
    ... }
    >>> data = form.extract(request)    
    >>> data.printtree()
    <RuntimeData myform, value=<UNSET>, extracted=odict([('image', <UNSET>)]) at ...>
      <RuntimeData myform.image, value='\x89PNG\r\n...\x00IEND\xaeB`\x82', extracted=<UNSET> at ...>
    
    >>> pxml(form(data=data))
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
    
    >>> request = {
    ...     'myform.image': '123',
    ...     'myform.image-action': 'keep'
    ... }
    >>> data = form.extract(request)    
    >>> data.printtree()
    <RuntimeData myform, value=<UNSET>, extracted=odict([('image', '\x89PNG\r\n\...\x00IEND\xaeB`\x82')]) at ...>
      <RuntimeData myform.image, value='\x89PNG\r\n\...\x00IEND\xaeB`\x82', extracted='\x89PNG\r\n\...\x00IEND\xaeB`\x82' at ...>
    
    >>> request['myform.image-action'] = 'replace'
    >>> data = form.extract(request)
    >>> data.extracted
    odict([('image', '123')])
    
    >>> request['myform.image-action'] = 'delete'
    >>> data = form.extract(request)
    >>> data.extracted
    odict([('image', <UNSET>)])
