from importlib.metadata import version

try:
    __version__ = version("django-voting")
except Exception:
    # package is not installed
    __version__ = None
