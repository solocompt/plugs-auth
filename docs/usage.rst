=====
Usage
=====

To use Plugs Auth in a project, add it to your `INSTALLED_APPS`:

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
