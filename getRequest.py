from dotenv import load_dotenv
from urllib.parse import quote
import aiohttp
import asyncio
import time
import os
import json
main_path = None
async def request_fb(fb_api_url=None, rpaths=[], dict_t_main = {}):
    #time.sleep(0.100)
    paths=None
    load_dotenv()
    token = os.getenv('TOKEN')
    fb_url = os.getenv('FB_URL')
    fb_url_split = fb_url.split('share')
    if fb_api_url==None:
        fb_api_url = f'{fb_url_split[0]}api/public/share{fb_url_split[1]}'
    fb_pass = os.getenv('FB_PASS')
    fb_headers = {'X-SHARE-PASSWORD': fb_pass}

    try:
        async with aiohttp.ClientSession() as session:
            resp = await session.get(fb_api_url, headers=fb_headers)
            data = await resp.json()
    except aiohttp.ClientError as e:
        print(f'Deu ruim {e}')

    items = data['items']

    for item in items:
        is_dir = item['isDir']
        path = item['path']
        name = item['name']
        #print(f'{fb_api_url}/{quote(name)}')
        if is_dir:
            link = f'{fb_api_url}/{quote(name)}'
            #links.append(asyncio.create_task(request_fb(fb_api_url=link)))
            await request_fb(fb_api_url=link)
        else:
            paths = path.split('/')[1:]
            #print(paths)
            rpaths.append(paths)
    dict_t = dict_t_main
    if paths:
        for item in paths[:-1]:
            if item not in dict_t:
                dict_t[item] = {}
                dict_t = dict_t[item]
        dict_t[paths[-1]] = 'link'
    with open('tree_pura.json', 'w') as t:
        t.write(json.dumps(dict_t_main, indent=2))

    print(json.dumps(dict_t_main, indent=2))
    print()
    return dict_t_main
            

    
async def main():
    start = time.time()

    #response = await request_fb()
    dict_complete = await request_fb(fb_api_url=None)
    print(dict_complete)

    end = time.time()
    total_time = end - start
    print(f"Código finalizado em {total_time} secs")

asyncio.run(main())
