"""Documentation."""
from ._API import *
# ======================================================================
def __getattr__(name: str) -> str:
    if name == '__version__':
        from importlib import metadata
        return metadata.version(__package__)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
__version__ = '0.1.0'
