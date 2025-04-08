"""
Simply store provenance in data produced by python scripts
"""
# {# pkglts, src
# FYEO
# #}
# {# pkglts, version, after src
from . import version

__version__ = version.__version__
# #}

from .provenance import *
