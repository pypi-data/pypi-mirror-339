"""aiprep - A tool for preparing files for AI interactions."""

try:
    from importlib.metadata import version
except ImportError:
    from importlib_metadata import version  # Python < 3.8

__version__ = version("aiprep")
