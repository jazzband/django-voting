=============
Django Voting
=============

This is a generic voting application for Django projects

For installation instructions, see the file "INSTALL.txt" in this
directory; for instructions on how to use this application, and on
what it provides, see the file "overview.txt" in the "docs/"
directory.


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
