Changelog
=========

Unreleased
----------

* Drop Django 3.0 support.
* Add Django 3.2 support.
* Add Python 3.10 support.
* Change ``Vote.object_id`` type to ``TextField`` to support
  other primary key types like ``UUIDField``.
* Drop Django 3.1 support.
* Add Django 4.0 support.

1.0 (2021-03-10)
----------------

* Replaced ``voting.VERSION`` with more canonical ``voting.__version__``.

* Added Django migrations.

* Drop South migrations.

* Add Django 2.2,  3.0, 3.1 support, drop support for all versions before that.

* Move CI to GitHub Actions: https://github.com/jazzband/django-voting/actions

0.2 (2012-07-26)
----------------

* Django 1.4 compatibility (timezone support)
* Added a ``time_stamp`` field to ``Vote`` model
* Added South migrations.
