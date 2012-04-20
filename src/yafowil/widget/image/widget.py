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
from yafowil.common import generic_required_extractor


@managedprops('image', *css_managed_props)
def image_edit_renderer(widget, data):
    return data.rendered


def image_extractor(widget, data):
    return data.extracted


def image_display_renderer(widget, data):
    return '<div>Image</div>'


factory.register(
    'image',
    extractors=[image_extractor, generic_required_extractor],
    edit_renderers=[image_edit_renderer],
    display_renderers=[image_display_renderer])

factory.doc['blueprint']['image'] = \
"""Add-on widget `yafowil.widget.image 
<http://github.com/bluedynamics/yafowil.widget.image/>`_.
"""

factory.defaults['image.class'] = 'image'

factory.defaults['image.required'] = False

factory.defaults['image.error_class'] = 'error'

factory.defaults['image.message_class'] = 'errormessage'