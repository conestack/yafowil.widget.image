import types
from PIL import Image
from yafowil.base import (
    UNSET,
    factory,
    fetch_value,
    ExtractionError,
)
from yafowil.utils import (
    cssid,
    css_managed_props,
    managedprops,
)
from yafowil.common import (
    generic_required_extractor,
    file_extractor,
    input_file_edit_renderer,
    file_options_renderer,
)


@managedprops('image', *css_managed_props)
def image_edit_renderer(widget, data):
    if not widget.attrs['src']:
        return data.rendered
    tag = data.tag
    img_attrs = {
        'src': widget.attrs['src'],
        'alt': widget.attrs['alt'],
        'id': cssid(widget, 'image-preview'),
        'class': 'image-preview',
    }
    img = tag('img', **img_attrs)
    return img + data.rendered


def mimetype_extractor(widget, data):
    """XXX: Move relevant parts to ``yafowil.common.mimetype_extractor``.
    """
    accept = widget.attrs['accept']
    if not accept:
        return data.extracted
    if not accept.startswith('image'):
        raise ValueError(u"Incompatible mimetype %s" % accept)
    mimetype = data.extracted['mimetype']
    if not mimetype.startswith('image'):
        raise ExtractionError(u"Uploaded file is not an image.")
    if accept[6:] == '*':
        return data.extracted
    if accept != mimetype:
        raise ExtractionError(u"Uploaded image not of type %s" % accept[6:])
    return data.extracted


def image_extractor(widget, data):
    """Creates a PIL image for subsequent extractors and set it to extracted
    data at key ``image``.
    """
    if data.extracted and \
       data.extracted['file']:
        data.extracted['image'] = Image.open(data.extracted['file'])
        data.extracted['file'].seek(0)
    return data.extracted


def size_extractor(widget, data):
    minsize = widget.attrs['minsize']
    maxsize = widget.attrs['maxsize']
    if not minsize and not maxsize:
        return data.extracted
    size = data.extracted['image'].size
    if minsize:
        if size[0] < minsize[0] or size[1] < minsize[1]:
            raise ExtractionError(
                u"Image must have a minimum size of %s x %s pixel" % \
                    (minsize[0], minsize[1]))
    if maxsize:
        if size[0] > maxsize[0] or size[1] > maxsize[1]:
            raise ExtractionError(
                u"Image must have a maximum size of %s x %s pixel" % \
                    (maxsize[0], maxsize[1]))
    return data.extracted


def dpi_extractor(widget, data):
    mindpi = widget.attrs['mindpi']
    maxdpi = widget.attrs['maxdpi']
    if not mindpi and not maxdpi:
        return data.extracted
    dpi = data.extracted['image'].info['dpi']
    if mindpi:
        if dpi[0] < mindpi[0] or dpi[1] < mindpi[1]:
            raise ExtractionError(
                u"Image must have at least %s x %s DPI" % \
                    (mindpi[0], mindpi[1]))
    if maxdpi:
        if dpi[0] > maxdpi[0] or dpi[1] > maxdpi[1]:
            raise ExtractionError(
                u"Image must have a maximum of %s x %s DPI" % \
                    (maxdpi[0], maxdpi[1]))
    return data.extracted


def crop_ectractor(widget, data):
    return data.extracted


def scales_extractor(widget, data):
    return data.extracted


def image_display_renderer(widget, data):
    if widget.attrs['src']:
        tag = data.tag
        img_attrs = {
            'src': widget.attrs['src'],
            'alt': widget.attrs['alt'],
        }
        return tag('img', **img_attrs)
    return data.rendered


factory.register(
    'image',
    extractors=[
        generic_required_extractor,
        file_extractor,
        mimetype_extractor,
        image_extractor,
        size_extractor,
        dpi_extractor,
        crop_ectractor,   
        scales_extractor],
    edit_renderers=[
        input_file_edit_renderer,
        file_options_renderer,
        image_edit_renderer],
    display_renderers=[
        image_display_renderer])

factory.doc['blueprint']['image'] = \
"""Add-on widget `yafowil.widget.image 
<http://github.com/bluedynamics/yafowil.widget.image/>`_.
"""

factory.defaults['image.class'] = 'image'

factory.defaults['image.required'] = False

factory.defaults['image.error_class'] = 'error'

factory.defaults['image.message_class'] = 'errormessage'

factory.defaults['image.vocabulary'] = [
    ('keep', u'Keep Existing image'),
    ('replace', u'Replace existing image'),
    ('delete', u'Delete existing image'),
]

factory.defaults['image.alt'] = ''
factory.doc['props']['image.alt'] = """\
Image alternative text.
"""

factory.defaults['image.src'] = None
factory.doc['props']['image.src'] = """\
Image URL if image present and displaying is desired.
"""

factory.defaults['image.accept'] = 'image/*'
factory.doc['props']['image.accept'] = """\
Accepted mimetype of image.
"""

factory.defaults['image.minsize'] = None
factory.doc['props']['image.minsize'] = """\
Minimum size of image defined as 2-tuple containing (width, height) in
pixel as integer.
"""

factory.defaults['image.maxsize'] = None
factory.doc['props']['image.maxsize'] = """\
Maximum size of image defined as 2-tuple containing (width, height) in
pixel as integer.
"""

factory.defaults['image.mindpi'] = None
factory.doc['props']['image.mindpi'] = """\
Minimum DPI of image defined as 2-tuple containing (x, y).
"""

factory.defaults['image.maxdpi'] = None
factory.doc['props']['image.maxdpi'] = """\
Maximum DPI of image defined as 2-tuple containing (x, y).
"""

factory.defaults['image.crop'] = None
factory.doc['props']['image.crop'] = """\
Crop extracted file to size defined as 2-tuple containing (width, height) in
pixel as integer. The created cropped image gets placed in the return value 
returned by file extractor under key ``cropped``.
"""

factory.defaults['image.scales'] = None
factory.doc['props']['image.scales'] = """\
Scales to create on extraction. Scales are defined as dict, where the key
represents the scale name and the value is a 2-tuple containing (width, height)
in pixel as integer. The created scales get placed in the return value returned
by file extractor under key ``scales``.
"""