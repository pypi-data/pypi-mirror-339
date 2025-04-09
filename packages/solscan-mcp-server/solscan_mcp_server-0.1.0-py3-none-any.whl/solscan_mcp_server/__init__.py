import logging
import sys

import click

from .server import serve


@click.command()
@click.option(
    "--api-key", "-k", type=str, envvar="SOLSCAN_API_KEY", help="Solscan Pro API key"
)
@click.option("-v", "--verbose", count=True)
def main(api_key: str | None, verbose: bool) -> None:
    """MCP Solscan Server - Solscan Pro API functionality for MCP"""
    import asyncio

    if not api_key:
        raise click.ClickException(
            "Solscan API key is required. Set it via --api-key or SOLSCAN_API_KEY environment variable"
        )

    logging_level = logging.WARN
    if verbose == 1:
        logging_level = logging.INFO
    elif verbose >= 2:
        logging_level = logging.DEBUG

    logging.basicConfig(level=logging_level, stream=sys.stderr)

    asyncio.run(serve(api_key))


if __name__ == "__main__":
    main()
