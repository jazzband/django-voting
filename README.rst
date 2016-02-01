=============
Django Voting
=============

This is a generic voting application for Django projects


Installation
============

1. Install the ``django-voting`` distribution

2. Add ``voting`` to your ``INSTALLED_APPS``::

    INSTALLED_APPS = [
        …
        'voting',
        …
    ]

3. Run ``django-admin migrate``


Usage
=====

See "overview.txt" in the "docs/" directory.


Test suite
==========

The tests can be run with Django's test runner::

    django-admin test tests


or with pytest::

    pip install pytest-django
    py.test


Coverage
--------

A code coverage report can be collected directly with ``coverage``::

    pip install coverage
    coverage run $(which django-admin) test tests
    coverage report
    coverage html


or with pytest::

    pip install pytest-cov
    py.test --cov
    py.test --cov --cov-report=html
