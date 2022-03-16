import asyncio
import argparse
import os

import aiohttp
import aiofiles


async def download_site(url, session, file_name):
    async with session.get(url) as response:
        if response.status == 200:
            async with aiofiles.open(file_name, mode="wb") as file:
                await file.write(await response.read())


async def download_all_sites(sites, path_to_files):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for image_number, url in enumerate(sites):
            task = asyncio.create_task(download_site(url, session, f"{path_to_files}/image_{image_number}.jpg"))
            tasks.append(task)
        try:
            await asyncio.gather(*tasks, return_exceptions=True)
        except Exception as ex:
            print(repr(ex))


def make_arguments_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--num', type=int, default=10)
    parser.add_argument('--dir', type=str, default="artifacts")
    return parser


if __name__ == '__main__':
    parser = make_arguments_parser()
    args = parser.parse_args()

    if not os.path.exists(args.dir):
        os.makedirs(args.dir)

    sites = ["https://picsum.photos/200/300"] * args.num

    loop = asyncio.get_event_loop()
    try:
        task = loop.create_task(download_all_sites(sites, args.dir))
        loop.run_until_complete(task)
    finally:
        loop.close()
