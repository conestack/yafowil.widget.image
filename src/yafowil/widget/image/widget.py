import types
import time
from PIL import Image
from imageutils.size import (
    scale_size,
    aspect_ratio_approximate,
    same_aspect_ratio,
)
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


@managedprops('src', 'alt', *css_managed_props)
def image_edit_renderer(widget, data):
    src = widget.attrs['src']
    if callable(src):
        src = src(widget, data)
    if not src:
        return data.rendered
    src = src + '?nocache=%i' % time.time()
    tag = data.tag
    img_attrs = {
        'src': src,
        'alt': widget.attrs['alt'],
        'id': cssid(widget, 'image-preview'),
        'class': 'image-preview',
    }
    img = tag('img', **img_attrs)
    return img + data.rendered


@managedprops('accept')
def mimetype_extractor(widget, data):
    """XXX: Move relevant parts to ``yafowil.common.mimetype_extractor``.
    """
    accept = widget.attrs['accept']
    if not data.extracted or not accept:
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
    if data.extracted and data.extracted['file']:
        data.extracted['image'] = Image.open(data.extracted['file'])
        data.extracted['file'].seek(0)
    if data.extracted is UNSET:
        # None means submitted but no upload
        return None
    return data.extracted


@managedprops('minsize', 'maxsize')
def size_extractor(widget, data):
    minsize = widget.attrs['minsize']
    maxsize = widget.attrs['maxsize']
    if not minsize and not maxsize:
        return data.extracted
    if data.extracted and data.extracted.get('image'):
        size = data.extracted['image'].size
        if minsize == maxsize:
            if size[0] != minsize[0] or size[1] != minsize[1]:
                raise ExtractionError(
                    u"Image must have a size of %s x %s pixel" % \
                        (minsize[0], minsize[1]))
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


@managedprops('mindpi', 'maxdpi')
def dpi_extractor(widget, data):
    mindpi = widget.attrs['mindpi']
    maxdpi = widget.attrs['maxdpi']
    if not mindpi and not maxdpi:
        return data.extracted
    if data.extracted and data.extracted.get('image'):
        dpi = data.extracted['image'].info['dpi']
        if mindpi == maxdpi:
            if dpi[0] != mindpi[0] or dpi[1] != mindpi[1]:
                raise ExtractionError(
                    u"Image must have a resolution of %s x %s DPI" % \
                        (mindpi[0], mindpi[1]))
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


@managedprops('scales')
def scales_extractor(widget, data):
    scales = widget.attrs['scales']
    if not scales or not data.extracted or not data.extracted.get('image'):
        return data.extracted
    image = data.extracted['image']
    scaled_images = dict()
    image_appr = aspect_ratio_approximate(image.size)
    for name, size in scales.items():
        scale_appr = aspect_ratio_approximate(size)
        if same_aspect_ratio(size, image.size):
            image_size = size
        # scale x
        if image_appr > scale_appr:
            image_size = scale_size(image.size, (size[0], None))
        # scale y
        if image_appr < scale_appr:
            image_size = scale_size(image.size, (None, size[1]))
        scaled_images[name] = image.resize(image_size, Image.ANTIALIAS)
    data.extracted['scales'] = scaled_images
    return data.extracted


@managedprops('crop')
def crop_extractor(widget, data):
    """XXX:
    - support cropping definitions as request parameters.
        left, top, width, height (for use with JS cropping plugin)
    - alignment
        tl (top left), tr (top right), bl (bottom left),
        br (bottom right), ce (center), rc (right center),
        lc (left center), tc (top center), bc (bottom center)
    """
    crop = widget.attrs['crop']
    if not crop or not data.extracted or not data.extracted.get('image'):
        return data.extracted
    size = crop['size']
    offset = crop.get('offset', (0, 0))
    fitting = crop.get('fitting', False)
    image = data.extracted['image']
    image_appr = aspect_ratio_approximate(image.size)
    crop_appr = aspect_ratio_approximate(size)
    if fitting:
        if same_aspect_ratio(size, image.size):
            image = image.resize(size, Image.ANTIALIAS)
            offset = (0, 0)
        # scale x
        if image_appr < crop_appr:
            image_size = scale_size(image.size, (size[0], None))
            image = image.resize(image_size, Image.ANTIALIAS)
            offset = (0, (image_size[1] - size[1]) / 2)
        # scale y
        if image_appr > crop_appr:
            image_size = scale_size(image.size, (None, size[1]))
            image = image.resize(image_size, Image.ANTIALIAS)
            offset = ((image_size[0] - size[0]) / 2, 0)
    image = image.crop(
        (offset[0], offset[1], size[0] + offset[0], size[1] + offset[1]))
    data.extracted['cropped'] = image
    return data.extracted


@managedprops('src', 'alt')
def image_display_renderer(widget, data):
    src = widget.attrs['src']
    if src:
        if callable(src):
            src = src(widget, data)
        tag = data.tag
        img_attrs = {
            'src': src,
            'alt': widget.attrs['alt'],
        }
        return tag('img', **img_attrs)
    return ''


factory.register(
    'image',
    extractors=[
        file_extractor,
        generic_required_extractor,
        mimetype_extractor,
        image_extractor,
        size_extractor,
        dpi_extractor,
        scales_extractor,
        crop_extractor],
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

factory.defaults['image.scales'] = None
factory.doc['props']['image.scales'] = """\
Scales to create on extraction. Scales are defined as dict, where the key
represents the scale name and the value is a 2-tuple containing (width, height)
in pixel. The created scales get placed in the return value returned by file
extractor under key ``scales``.
"""

factory.defaults['image.crop'] = None
factory.doc['props']['image.crop'] = """\
Crop extracted file to size at offset. The created cropped image gets placed
in the return value returned by file extractor under key ``cropped``. Crop
definition is a dict containing:

size
    (width, height), mandatory
offset
    (left, top), defaults to (0, 0)
fitting
    Boolean, ignores offset if True, scales image to smaller site of ``size``
    and centers larger one.
"""