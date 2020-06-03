import aiohttp
import asyncio
import random
import requests
import sys
from timeit import default_timer

from .user_agents import USER_AGENTS

"""
Compare fetching urls sequentially using Requests vs asynchronously using aiohttp.

Requirements:
    Python3.7+ -> `asyncio.create_task`, `aysnc.run`
    requests
    aiohttp
    click
"""
class UrlFetcher:

    URLS = [
        "https://apple.com",
        "https://bing.com",
        "https://github.com",
        "https://google.com",
        "https://yahoo.com",
    ]

    def __init__(self):
        self.async_tasks = []
        self.url_times = dict()

    async def fetch(self, url):
        """Create a task to fetch a url asynchronously.
        Each task creates its own ClientSession to fetch with different
        headers."""
        headers = self._get_random_user_agent()
        self.url_times[url] = default_timer()
        async with aiohttp.ClientSession(headers=headers) as session:
            resp = await session.get(url)
            self.url_times[url] = default_timer() - self.url_times[url]
            return resp

    async def async_main(self):
        start = default_timer()
        for url in self.URLS:
            task = asyncio.create_task(self.fetch(url))
            self.async_tasks.append(task)

        responses = await asyncio.gather(*self.async_tasks)
        total_time = default_timer() - start
        self._print_timings()
        print("-"*10)
        print(f"total time: {total_time}")
        return total_time

    def _get_random_user_agent(self):
        return {
            "User-Agent": random.choice(USER_AGENTS)
        }

    def _print_timings(self):
        for url, fetch_time in self.url_times.items():
            print("'{0}': {1:5.2f} sec.".format(url, fetch_time))

    def seq_main(self):
        responses = []
        start = default_timer()
        for url in self.URLS:
            headers = self._get_random_user_agent()

            url_start = default_timer()
            # using requests content manager to match aiohttp logic
            with requests.Session() as session:
                responses.append(session.get(url))
                self.url_times[url] = default_timer() - url_start

        total_time = default_timer() - start
        self._print_timings()
        print("-"*10)
        print(f"total time: {total_time}")
        return total_time


if __name__ == "__main__":
    main()
