"""
MCP server implementation for Coze API
"""

import asyncio

from .server import CozeServer, mcp
from .version import __version__

def main():
    asyncio.run(mcp.run_stdio_async())

if __name__ == "__main__":
    main()

__all__ = ["CozeServer", "main", "__version__"] 