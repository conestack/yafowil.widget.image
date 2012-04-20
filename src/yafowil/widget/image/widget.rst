Import requirements::

    >>> import PIL
    >>> import yafowil.loader
    >>> import yafowil.widget.image
    >>> from yafowil.base import factory

Create image form::

    >>> form = factory(
    ...     'form',
    ...     name='myform',
    ...     props={'action': 'myaction'})
    >>> pxml(form())
    <form action="myaction" enctype="multipart/form-data" id="form-myform" method="post" novalidate="novalidate"/>
    <BLANKLINE>
