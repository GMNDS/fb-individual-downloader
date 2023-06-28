import aiohttp
import asyncio
import time
import os
from dotenv import load_dotenv
import json


async def request_fb(fb_api_url, fb_headers):
    print('iniciando código')
    
    async with aiohttp.ClientSession() as session:
        print('pegando dados da api')
        resp = await session.get(fb_api_url, headers=fb_headers)
        data = await resp.json()

    items = data['items']
    main_path = data['name']
    have_dir=False

    fb_json = {}
    links_p = []

    for item in items:
        isDir = item['isDir']
        path = item['path']
        name = item['name']
        if main_path in fb_json:
            fb_json[main_path].append(path if isDir else name)
            link_dir = f'{fb_api_url}{path}'
            links_p.append(link_dir) if isDir else None
            have_dir=True
        else:
            fb_json[main_path] = [path if isDir else name]
    return {
        'have_dir': have_dir,
        'fb_json': fb_json,
        'links': links_p
    }


async def process_fb():
    load_dotenv()
    fb_pass = os.getenv('FB_PASS')
    fb_api_url = os.getenv('FB_URL')
    fb_headers = {'X-SHARE-PASSWORD': fb_pass}
    fb_tree = await request_fb(fb_api_url, fb_headers)
    have_dir = fb_tree['have_dir']
    fb_json = fb_tree['fb_json']
    links = fb_tree['links']
    #print(links, sep="\n\n")

    tasks = []

    for link in links:
        tasks.append(request_fb(link, fb_headers))


    fb_jsons = []

    if have_dir:
        fb_jsons.append(fb_json)
        responses = await asyncio.gather(*tasks)
        test = {"animes": []}
        for response in responses:
            test['animes'].append(response['fb_json'])
        with open('test.json', 'w') as f:
                json_data = json.dumps(test, indent=4)
                f.write(json_data)
            



    #print(fb_jsons, sep="\n\n")
        



async def main():
    start = time.time()

    await process_fb()

    end = time.time()
    total_time = end - start
    print(f"Código finalizado em {total_time} secs")

asyncio.run(main())
