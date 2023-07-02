import aiohttp
import asyncio
import time
import os
from dotenv import load_dotenv
import json


async def request_fb(fb_api_url=None):
    load_dotenv()
    fb_url = os.getenv('FB_URL')
    fb_url_split = fb_url.split('share')
    if fb_api_url==None:
        fb_api_url = f'{fb_url_split[0]}api/public/share{fb_url_split[1]}'
    fb_pass = os.getenv('FB_PASS')
    fb_headers = {'X-SHARE-PASSWORD': fb_pass}

    
    async with aiohttp.ClientSession() as session:
        #print('pegando dados da api')
        resp = await session.get(fb_api_url, headers=fb_headers)
        data = await resp.json()

    items = data['items']
    main_path = data['name']

    for item in items:
        is_dir = item['isDir']
        path = item['path']
        name = item['name']

        if is_dir:
            link = f'{fb_api_url}/{name}'
            await request_fb(fb_api_url=link)
            #print(link)
        else:
            pathsplit = path.split('/')
            link = f'{fb_api_url}{path}'
            #print(f'{link}/{name}')
            print(pathsplit[:-1])

            
    
async def main():
    start = time.time()

    await request_fb()

    end = time.time()
    total_time = end - start
    print(f"Código finalizado em {total_time} secs")

asyncio.run(main())
