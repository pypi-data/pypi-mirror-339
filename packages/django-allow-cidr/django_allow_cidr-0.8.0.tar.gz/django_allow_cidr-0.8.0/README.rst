Django Allow CIDR
=================

.. image:: https://img.shields.io/pypi/v/django-allow-cidr.svg
    :target: https://pypi.org/project/django-allow-cidr/

.. image:: https://github.com/mozmeao/django-allow-cidr/actions/workflows/ci.yml/badge.svg
    :target: https://github.com/mozmeao/django-allow-cidr/actions


A Django Middleware to enable use of CIDR IP ranges in ALLOWED_HOSTS.

Quickstart
----------

Install Django Allow CIDR::

    pip install django-allow-cidr

Add the Middleware to your ``MIDDLEWARE`` settings. It should be the first in the list:

.. code-block:: python

    MIDDLEWARE = (
        'allow_cidr.middleware.AllowCIDRMiddleware',
        ...
    )

Add the ``ALLOWED_CIDR_NETS`` setting:

.. code-block:: python

    ALLOWED_CIDR_NETS = ['192.168.1.0/24']

Profit!

Features
--------

* The normal ``ALLOWED_HOSTS`` values will also work as intended. This Middleware is intended to augment,
  not replace, the normal Django function.
* If you do define ``ALLOWED_CIDR_NETS`` and it has values, the middleware will capture what you have in ``ALLOWED_HOSTS``,
  set ``ALLOWED_HOSTS`` to ``['*']`` and take over validation of host headers.
* The ``ALLOWED_CIDR_NETS`` values can be any valid network definition for the `ipaddress`_ library.

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox


Pushing to PyPI
---------------
Cutting a new Github Release will trigger CI checks, followed by an automatic release to PyPI, using the release version.
Please make sure that your Github Release version matches the project version in ``__init__.py``.

For more details see the ``release`` job in  ``.github/workflows/ci.yml``.


Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _ipaddress: https://docs.python.org/3/library/ipaddress.html
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
