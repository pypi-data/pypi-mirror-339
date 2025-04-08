from .server import serve


def main():
    """MCP Deepthinking main entry point."""
    import asyncio
    asyncio.run(serve())


if __name__ == "__main__":
    main()