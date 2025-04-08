Wagtail case insensitive redirects
==================================

Fixes case errors in URLs by redirecting.

Installation
------------

.. code:: shell

    pip install wagtail-case-insensitive

Usage
-----

In your project’s Django settings file:

.. code:: python

    INSTALLED_APPS = [
        # ...

        'case_insensitive',
    ]

    MIDDLEWARE = [
        # ...
        # all other django middleware first

        'case_insensitive.middleware.CaseInsensitiveRouteMiddleware',
    ]


Then replace :code:`wagtail.models.Page` with :code:`case_insensitive.models.CaseInsensitiveRoutePage`:

.. code:: python

    from case_insensitive.models import CaseInsensitiveRoutePage as Page


    class MyContentPage(Page):
        ...
