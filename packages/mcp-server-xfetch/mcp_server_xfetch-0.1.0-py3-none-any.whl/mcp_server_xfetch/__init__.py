from .server import serve


def main():
    """MCP XFetch Server - HTTP fetching functionality for MCP"""
    import argparse
    import asyncio

    parser = argparse.ArgumentParser(
        description="Enhanced web content fetching for MCP with Cloudflare bypass and JavaScript rendering"
    )
    parser.add_argument(
        "--api-token",
        type=str,
        help="API token for xfetch.ai service. Can also be set via XFETCH_API_TOKEN environment variable.",
    )
    args = parser.parse_args()
    asyncio.run(serve(api_token=args.api_token))


if __name__ == "__main__":
    main()
