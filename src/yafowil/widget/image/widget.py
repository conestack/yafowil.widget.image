from PIL import Image
from node.utils import UNSET
from yafowil.base import ExtractionError
from yafowil.base import factory
from yafowil.common import file_extractor
from yafowil.common import file_options_renderer
from yafowil.common import generic_required_extractor
from yafowil.common import input_file_edit_renderer
from yafowil.tsf import TSF
from yafowil.utils import attr_value
from yafowil.utils import css_managed_props
from yafowil.utils import cssid
from yafowil.utils import managedprops
from yafowil.widget.image.utils import aspect_ratio_approximate
from yafowil.widget.image.utils import same_aspect_ratio
from yafowil.widget.image.utils import scale_size
import time


_ = TSF('yafowil.widget.dict')


@managedprops('src', 'alt', *css_managed_props)
def image_edit_renderer(widget, data):
    src = attr_value('src', widget, data)
    if not src:
        return data.rendered
    if src.find('?') > -1:
        src = src + '&amp;nocache=%i' % time.time()
    else:
        src = src + '?nocache=%i' % time.time()
    tag = data.tag
    img_attrs = {
        'src': src,
        'alt': attr_value('alt', widget, data),
        'id': cssid(widget, 'image-preview'),
        'class': 'image-preview',
    }
    img = tag('img', **img_attrs)
    return img + data.rendered


@managedprops('accept')
def mimetype_extractor(widget, data):
    """XXX: Move relevant parts to ``yafowil.common.mimetype_extractor``.
    """
    accept = attr_value('accept', widget, data)
    if not data.extracted or not accept:
        return data.extracted
    if not accept.startswith('image'):
        raise ValueError(u"Incompatible mimetype %s" % accept)
    mimetype = data.extracted['mimetype']
    if not mimetype.startswith('image'):
        message = _('file_not_an_image',
                    default=u'Uploaded file is not an image.')
        raise ExtractionError(message)
    if accept[6:] == '*':
        return data.extracted
    if accept != mimetype:
        message = _('file_invalid_type',
                    default=u'Uploaded image not of type ${type}',
                    mapping={'type': accept[6:]})
        raise ExtractionError(message)
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
    minsize = attr_value('minsize', widget, data)
    maxsize = attr_value('maxsize', widget, data)
    if not minsize and not maxsize:
        return data.extracted
    if data.extracted and data.extracted.get('image'):
        size = data.extracted['image'].size
        if minsize == maxsize:
            if size[0] != minsize[0] or size[1] != minsize[1]:
                message = _('exact_image_size_required',
                            default=u'Image must have a size of '
                                    u'${width} x ${height} pixel',
                            mapping={
                                'width': minsize[0],
                                'height': minsize[1],
                            })
                raise ExtractionError(message)
        if minsize:
            if size[0] < minsize[0] or size[1] < minsize[1]:
                message = _('minimum_image_size_required',
                            default=u'Image must have a minimum size of '
                                    u'${width} x ${height} pixel',
                            mapping={
                                'width': minsize[0],
                                'height': minsize[1],
                            })
                raise ExtractionError(message)
        if maxsize:
            if size[0] > maxsize[0] or size[1] > maxsize[1]:
                message = _('maximum_image_size_required',
                            default=u'Image must have a maximum size of '
                                    u'${width} x ${height} pixel',
                            mapping={
                                'width': maxsize[0],
                                'height': maxsize[1],
                            })
                raise ExtractionError(message)
    return data.extracted


@managedprops('mindpi', 'maxdpi')
def dpi_extractor(widget, data):
    mindpi = attr_value('mindpi', widget, data)
    maxdpi = attr_value('maxdpi', widget, data)
    rounddpi = attr_value('rounddpi', widget, data)
    if not mindpi and not maxdpi:
        return data.extracted
    if data.extracted and data.extracted.get('image'):
        dpi = data.extracted['image'].info['dpi']
        if rounddpi:
            dpi = [round(dpi[0]), round(dpi[1])]
        if mindpi == maxdpi:
            if dpi[0] != mindpi[0] or dpi[1] != mindpi[1]:
                message = _('exact_image_dpi_required',
                            default=u'Image must have a resolution of '
                                    u'${width} x ${height} DPI',
                            mapping={
                                'width': mindpi[0],
                                'height': mindpi[1],
                            })
                raise ExtractionError(message)
        if mindpi:
            if dpi[0] < mindpi[0] or dpi[1] < mindpi[1]:
                message = _('minimum_image_dpi_required',
                            default=u'Image must have at least '
                                    u'${width} x ${height} DPI',
                            mapping={
                                'width': mindpi[0],
                                'height': mindpi[1],
                            })
                raise ExtractionError(message)
        if maxdpi:
            if dpi[0] > maxdpi[0] or dpi[1] > maxdpi[1]:
                message = _('maximum_image_dpi_required',
                            default=u'Image must have a maximum of '
                                    u'${width} x ${height} DPI',
                            mapping={
                                'width': maxdpi[0],
                                'height': maxdpi[1],
                            })
                raise ExtractionError(message)
    return data.extracted


@managedprops('scales')
def scales_extractor(widget, data):
    scales = attr_value('scales', widget, data)
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
    crop = attr_value('crop', widget, data)
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
    src = attr_value('src', widget, data)
    if src:
        tag = data.tag
        img_attrs = {
            'src': src,
            'alt': attr_value('alt', widget, data),
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

factory.doc['blueprint']['image'] = """\
Add-on widget `yafowil.widget.image
<http://github.com/conestack/yafowil.widget.image/>`_.
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

factory.defaults['image.rounddpi'] = True
factory.doc['props']['image.rounddpi'] = """\
Round DPI values from image for extraction.

Pillow, as of version 6.0, no longer rounds reported DPI values for BMP, JPEG
and PNG images, but image manipulation programs may not produce accurate DPI
values.
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
