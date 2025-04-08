try:
    from ._version import version as __version__
except ImportError:
    # Package is not installed
    __version__ = "0.0.0+unknown"

from .mojo_arrow_sys import arrow_stream
