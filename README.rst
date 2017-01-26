=============================
Plugs Auth
=============================

.. image:: https://badge.fury.io/py/plugs-auth.png
    :target: https://badge.fury.io/py/plugs-auth

.. image:: https://travis-ci.org/ricardolobo/plugs-auth.png?branch=master
    :target: https://travis-ci.org/ricardolobo/plugs-auth

Your project description goes here

Documentation
-------------

The full documentation is at https://plugs-auth.readthedocs.io.

Quickstart
----------

Install Plugs Auth::

    pip install plugs-auth

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'plugs_auth.apps.PlugsAuthConfig',
        ...
    )

Add Plugs Auth's URL patterns:

.. code-block:: python

    from plugs_auth import urls as plugs_auth_urls


    urlpatterns = [
        ...
        url(r'^', include(plugs_auth_urls)),
        ...
    ]

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
