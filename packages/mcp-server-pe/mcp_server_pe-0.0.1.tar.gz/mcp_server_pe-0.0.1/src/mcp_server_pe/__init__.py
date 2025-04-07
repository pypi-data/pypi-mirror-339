import click
import logging
import sys
from .server import serve

@click.command()
@click.option("--api-token",  type=str, help="App api token")
@click.option("-v", "--verbose", count=True)
def main(api_token: str, verbose: bool) -> None:
    """MCP Git Server - Git functionality for MCP"""
    import asyncio

    logging_level = logging.WARN
    if verbose == 1:
        logging_level = logging.INFO
    elif verbose >= 2:
        logging_level = logging.DEBUG

    logging.basicConfig(level=logging_level, stream=sys.stderr)
    asyncio.run(serve(api_token=api_token))


if __name__ == "__main__":
    main()
