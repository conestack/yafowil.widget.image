from yafowil.base import factory
from yafowil.utils import entry_point
import os
import webresource as wr


resources_dir = os.path.join(os.path.dirname(__file__), 'resources')


##############################################################################
# Default
##############################################################################

# webresource ################################################################

resources = wr.ResourceGroup(
    name='yafowil.widget.image',
    directory=resources_dir,
    path='yafowil-image'
)
resources.add(wr.ScriptResource(
    name='yafowil-image-js',
    directory=os.path.join(resources_dir, 'default'),
    depends='jquery-js',
    resource='widget.js',
    compressed='widget.min.js'
))
resources.add(wr.StyleResource(
    name='yafowil-image-css',
    directory=os.path.join(resources_dir, 'default'),
    resource='widget.min.css'
))

# B/C resources ##############################################################

js = [{
    'group': 'yafowil.widget.image.common',
    'resource': 'default/widget.js',
    'order': 20,
}]
css = [{
    'group': 'yafowil.widget.image.common',
    'resource': 'default/widget.min.css',
    'order': 21,
}]


##############################################################################
# Registration
##############################################################################

@entry_point(order=10)
def register():
    from yafowil.widget.image import widget  # noqa

    widget_name = 'yafowil.widget.image'

    # Default
    factory.register_theme(
        'default',
        widget_name,
        resources_dir,
        js=js,
        css=css
    )
    factory.register_resources('default', widget_name, resources)
