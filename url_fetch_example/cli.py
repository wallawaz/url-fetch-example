from . import __version__, UrlFetcher

import asyncio
import click

@click.command()
@click.version_option(version=__version__)
@click.argument(
    "fetch-type",
    type=click.Choice(["requests", "aiohttp"]),
    required=True
)
def main(fetch_type):
    fetcher = UrlFetcher()
    if fetch_type == "requests":
        fetcher.seq_main()
    else:
        asyncio.run(fetcher.async_main())
