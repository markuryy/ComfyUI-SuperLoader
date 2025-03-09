"""Top-level package for superloader."""

__all__ = [
    "NODE_CLASS_MAPPINGS",
    "NODE_DISPLAY_NAME_MAPPINGS",
    "WEB_DIRECTORY",
]

__author__ = """Markury"""
__email__ = "comfy@markury.dev"
__version__ = "0.0.1"

from .src.superloader.nodes import NODE_CLASS_MAPPINGS
from .src.superloader.nodes import NODE_DISPLAY_NAME_MAPPINGS

WEB_DIRECTORY = "./web/js"
