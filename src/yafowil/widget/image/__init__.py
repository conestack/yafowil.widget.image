import os
from yafowil.base import factory


# XXX: use fanstatic
resourcedir = os.path.join(os.path.dirname(__file__), 'resources')

js = [{
    'group': 'yafowil.widget.image',
    'resource': 'widget.js',
    'order': 20,
}]

css = [{
    'group': 'yafowil.widget.image',
    'resource': 'widget.css',
    'order': 21,
}]


def register():
    import widget
    factory.register_theme('default', 'yafowil.widget.image',
                           resourcedir, js=js, css=css)