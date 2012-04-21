import types
from yafowil.base import (
    UNSET,
    factory,
    fetch_value,
)
from yafowil.utils import (
    cssid,
    cssclasses,
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
    }
    img = tag('img', **img_attrs)
    return img + data.rendered


def image_extractor(widget, data):
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
    extractors=[image_extractor, file_extractor, generic_required_extractor],
    edit_renderers=[
        image_edit_renderer, input_file_edit_renderer, file_options_renderer],
    display_renderers=[image_display_renderer])

factory.doc['blueprint']['image'] = \
"""Add-on widget `yafowil.widget.image 
<http://github.com/bluedynamics/yafowil.widget.image/>`_.
"""

factory.defaults['image.class'] = 'image'

factory.defaults['image.required'] = False

factory.defaults['image.error_class'] = 'error'

factory.defaults['image.message_class'] = 'errormessage'

factory.defaults['image.accept'] = 'image/*'

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