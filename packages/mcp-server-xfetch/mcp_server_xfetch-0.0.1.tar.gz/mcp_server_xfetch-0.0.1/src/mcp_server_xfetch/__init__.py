from .server import serve


def main():
    """MCP XFetch Server - HTTP fetching functionality for MCP"""
    import asyncio
    asyncio.run(serve())


if __name__ == "__main__":
    main()
