import os 


def register():
    import widget


def get_resource_dir():
    return os.path.join(os.path.dirname(__file__), 'resources')


def get_js():
    return [{
        'resource': 'widget.js',
        'thirdparty': False,
        'order': 20,
    }]


def get_css():
    return [{
        'resource': 'widget.css',
        'thirdparty': False,
        'order': 21,
    }]