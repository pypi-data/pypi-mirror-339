import click
import logging
import sys
from .server import serve

@click.command()
@click.option("--api-tokens", required=True, type=str, help="App api token, 多个token使用逗号分隔")
@click.option("-v", "--verbose", count=True)
def main(api_tokens: str, verbose: bool) -> None:
    """MCP Git Server - Git functionality for MCP"""
    import asyncio

    logging_level = logging.WARN
    if verbose == 1:
        logging_level = logging.INFO
    elif verbose >= 2:
        logging_level = logging.DEBUG

    logging.basicConfig(level=logging_level, stream=sys.stderr)
    asyncio.run(serve(api_tokens=api_tokens))


if __name__ == "__main__":
    main()
