import aiohttp
import asyncio
import time
import os
from dotenv import load_dotenv
import json
main_path = None

async def get_main_path(fb_api_url=None):
    global main_path
    if main_path is not None:
        return main_path
    else:
        load_dotenv()
        fb_url = os.getenv('FB_URL')
        fb_url_split = fb_url.split('share')
        if fb_api_url==None:
            fb_api_url = f'{fb_url_split[0]}api/public/share{fb_url_split[1]}'
        fb_pass = os.getenv('FB_PASS')
        fb_headers = {'X-SHARE-PASSWORD': fb_pass}

        
        async with aiohttp.ClientSession() as session:
            resp = await session.get(fb_api_url, headers=fb_headers)
            data = await resp.json()
            main_path = data['name']
            return main_path

async def request_fb(fb_api_url=None, rpaths=[]):
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

    main_path = await get_main_path()
    items = data['items']

    for item in items:
        is_dir = item['isDir']
        path = item['path']
        name = item['name']

        if is_dir:
            link = f'{fb_api_url}/{name}'
            await request_fb(fb_api_url=link)
            #print(link)
        else:
            paths = path.split('/')[1:]
            rpaths.append(paths)
    return rpaths
            

async def create_dict_fb(paths=None):
    dict_fb = {}
    if paths==None:
        paths = await request_fb(fb_api_url=None)
    
    for item in paths:
        chave = item[0]
        valores = item[1:]
        if len(valores) > 0:
            if chave not in dict_fb:
                dict_fb[chave] = (await create_dict_fb(paths=[valores]))
            else:
                dict_fb[chave].update(await create_dict_fb(paths=[valores]))
        else:
            dict_fb[chave] = {"name": chave, "link": "test"}
    print(dict_fb, end="\n\n")
    return dict_fb


    
async def main():
    start = time.time()

    #response = await request_fb()
    dados = await request_fb(fb_api_url=None)
    response = await create_dict_fb(dados)
    print(json.dumps(response, indent=4))
    #print(response)

    end = time.time()
    total_time = end - start
    print(f"Código finalizado em {total_time} secs")

asyncio.run(main())
