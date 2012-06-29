import os
import urlparse
from StringIO import StringIO
from yafowil.base import (
    factory,
    UNSET,
)


# XXX: more generic
try:
    from webob import Response
    def image_response(data):
        response = Response(content_type='image/jpg')
        response.write(data)
        return response
except ImportError:
    def image_response(url):
        return '' # XXX


# container for images during runtime.
runtime_images_dir = os.path.join(os.path.dirname(__file__), 'images_tmp')
if not os.path.exists(runtime_images_dir):
    os.mkdir(runtime_images_dir)


def read_image(name):
    image_path = os.path.join(runtime_images_dir, name + '.jpg')
    if not os.path.exists(image_path):
        data = ''
    else:
        with open(image_path) as fd:
            data = fd.read()
    return data


def get_image(environ, start_response):
    name = 'yafowil.widget.image.image'
    data = read_image(name)
    return image_response(data)(environ, start_response)


def save_image(widget, data):
    name = 'yafowil.widget.image.image'
    image = data.extracted[name]['image']
    image_path = os.path.join(runtime_images_dir, name + '.jpg')
    if image['action'] == 'keep':
        return
    if image['action'] == 'delete':
        os.remove(image_path)
        return
    image['scales']['default'].save(image_path, 'jpeg', quality=100)


DOC_IMAGE = """
Image
-----

Image widget.

Provide a form action handler storing images somewhere. File system is used in
this example.

.. code-block:: python

    runtime_images_dir = os.path.join(os.path.dirname(__file__), 'images_tmp')
    
    def save_image(widget, data):
        name = 'yafowil.widget.image.image'
        image = data.extracted[name]['image']
        image_path = os.path.join(runtime_images_dir, name + '.jpg')
        if image['action'] == 'keep':
            return
        if image['action'] == 'delete':
            os.remove(image_path)
            return
        # read from scales, see below
        image['scales']['default'].save(image_path, 'jpeg', quality=100)

The images should be available for the browser by URL in order to make image
blueprint work as expected.

Create widget.

.. code-block:: python

    name = 'yafowil.widget.image.image'
    image_name = name + '.jpg'
    image_path = os.path.join(runtime_images_dir, image_name)
    image_value = UNSET
    if os.path.exists(image_path):
        image_data = read_image(name)
        image_value = {'file': StringIO(image_data),
                       'mimetype': 'image/jpg'}
    form = factory('fieldset', name=name)
    form['image'] = factory('#field:image', value=image_value, props={
        'label': 'Image',
        'required': 'No Image uploaded',
        'maxsize': (1680, 1050),
        'scales': {'default': (300, 300)},
        'src': image_name,
        'error.class': 'help-block'})
"""

def image():
    name = 'yafowil.widget.image.image'
    image_name = name + '.jpg'
    image_path = os.path.join(runtime_images_dir, image_name)
    def get_value(widget, data):
        image_value = UNSET
        if os.path.exists(image_path):
            image_data = read_image(name)
            image_value = {'file': StringIO(image_data),
                           'mimetype': 'image/jpg'}
        return image_value
    def get_src(widget, data):
        if os.path.exists(image_path):
            return image_name
    form = factory('fieldset', name=name)
    form['image'] = factory('#field:image', value=get_value, props={
        'label': 'Image',
        'required': 'No Image uploaded',
        'maxsize': (1680, 1050),
        'scales': {'default': (300, 300)},
        'src': get_src,
        'error.class': 'help-block'})
    return {'widget': form,
            'doc': DOC_IMAGE,
            'title': 'Image',
            'handler': save_image,
            'routes': {image_name: get_image}}


def get_example():
    return [image()]
