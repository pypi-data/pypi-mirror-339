from . import server
import asyncio

def main():
    """Main entry point for the package."""
    asyncio.run(server.main())

__all__ = ['main', 'server']



# npx @modelcontextprotocol/inspector uv --directory /home/rag/python/yala-events run yala-events

