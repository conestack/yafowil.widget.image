from yafowil.base import factory

def get_example():
    part = factory(u'fieldset', name='yafowilwidgetimage')
    part['image'] = factory('field:label:error:image', props={})
    return [{'widget': part, 'doc': 'TODO'}]
