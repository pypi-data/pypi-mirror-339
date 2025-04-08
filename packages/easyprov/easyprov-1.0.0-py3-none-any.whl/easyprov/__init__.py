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

from .prov_csv import *
from .prov_json import *
from .prov_mpl import *
from .prov_rst import *
