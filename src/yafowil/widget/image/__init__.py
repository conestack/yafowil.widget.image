from yafowil.base import factory
from yafowil.utils import entry_point
import os
import webresource as wr


resources_dir = os.path.join(os.path.dirname(__file__), 'resources')


##############################################################################
# Default
##############################################################################

# webresource ################################################################

scripts = wr.ResourceGroup(name='yafowil-image-scripts')
scripts.add(wr.ScriptResource(
    name='yafowil-image-js',
    depends='jquery-js',
    directory=resources_dir,
    resource='widget.js',
    compressed='widget.min.js'
))

styles = wr.ResourceGroup(name='yafowil-image-styles')
styles.add(wr.StyleResource(
    name='yafowil-image-css',
    directory=resources_dir,
    resource='widget.css'
))

# B/C resources ##############################################################

js = [{
    'group': 'yafowil.widget.image.common',
    'resource': 'widget.js',
    'order': 20,
}]
css = [{
    'group': 'yafowil.widget.image.common',
    'resource': 'widget.css',
    'order': 21,
}]


##############################################################################
# Registration
##############################################################################

@entry_point(order=10)
def register():
    from yafowil.widget.image import widget  # noqa

    # Default
    factory.register_theme(
        'default', 'yafowil.widget.image', resources_dir,
        js=js, css=css
    )
    factory.register_scripts('default', 'yafowil.widget.image', scripts)
    factory.register_styles('default', 'yafowil.widget.image', styles)
