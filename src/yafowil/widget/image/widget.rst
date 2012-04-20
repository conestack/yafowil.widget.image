Import requirements::

    >>> import yafowil.loader
    >>> import yafowil.widget.image
    >>> from yafowil.base import factory

Create image form::

    >>> form = factory(
    ...     'form',
    ...     name='myform',
    ...     props={'action': 'myaction'})
    >>> pxml(form())