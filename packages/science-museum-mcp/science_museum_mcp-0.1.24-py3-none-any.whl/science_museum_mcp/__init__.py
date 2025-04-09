import sys
from .server import serve
import click
import logging

@click.command()
@click.option("-v", "--verbose")
def main(verbose: bool) -> None:
    import asyncio

    log_level = logging.DEBUG if verbose else logging.INFO

    logging.basicConfig(level=log_level, stream=sys.stderr)

    asyncio.run(serve())

if __name__ == "__main__":
    main()