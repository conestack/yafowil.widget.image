This is an **image widget** for for `YAFOWIL
<http://pypi.python.org/pypi/yafowil>`_ .


Example Application
===================

To run the example application and tests coming with this package run
`bootstrap <http://python-distribute.org/bootstrap.py>`_ (Python 2.6 or 2.7)
with a buildout like so:: 

    [buildout]
    parts = gunicorn   
    
    [tests]
    recipe = zc.recipe.testrunner
    eggs = 
        yafowil.widget.image[test]
    
    [gunicorn]
    recipe = zc.recipe.egg:scripts
    eggs = 
        ${test:eggs}
        gunicorn 
    
Start the application with::

   ./bin/gunicorn yafowil.widget.image.example:app

and connect with your webbrowser to ``http://localhost:8000/``

Run the tests with::

    ./bin/tests


Source Code
===========

The sources are in a GIT DVCS with its main branches at
`github <http://github.com/bluedynamics/yafowil.widget.image>`_.

We'd be happy to see many forks and pull-requests to make YAFOWIL even better.


Contributors
============

- Robert Niederreiter <rnix [at] squarewave [dot] at>
