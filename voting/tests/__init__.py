import django
if django.VERSION[0] == 1 and django.VERSION[1] < 6:
    from .tests import *
