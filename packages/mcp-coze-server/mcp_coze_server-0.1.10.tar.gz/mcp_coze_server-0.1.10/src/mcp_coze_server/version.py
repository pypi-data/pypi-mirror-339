"""Version information."""

import importlib.metadata

try:
    __version__ = importlib.metadata.version("mcp-coze-server")
except importlib.metadata.PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"

__all__ = ["__version__"] 