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
            if isDir:
                have_dir=True
            link_dir = f'{fb_api_url}/{name}'
            fb_json[main_path].append(path if isDir else link_dir)
            links_p.append(link_dir) if isDir else None
            
        else:
            fb_json[main_path] = [path if isDir else name]
            if isDir:
                have_dir=True
    return {
        'have_dir': have_dir,
        'fb_json': fb_json,
        'links': links_p
    }

fb_jsons = []
async def process_fb(fb_api_url=None ):
    load_dotenv()
    if fb_api_url==None:
        fb_api_url=os.getenv('FB_URL')
    fb_pass = os.getenv('FB_PASS')
    fb_headers = {'X-SHARE-PASSWORD': fb_pass}
    fb_tree = await request_fb(fb_api_url, fb_headers)
    have_dir = fb_tree['have_dir']
    fb_json = fb_tree['fb_json']
    links = fb_tree['links']
    #print(links, sep="\n\n")

    tasks = []

    for link in links:
        tasks.append(asyncio.create_task(process_fb(fb_api_url=link )))



    

    if have_dir:
        fb_jsons.append(fb_json)
        responses = await asyncio.gather(*tasks)
        test = {"animes": []}
        #print(json.dumps(responses, indent=4), end='\n\n')
        for response in responses:
            if response is not None:
                print(response)
                test['animes'].append(response)
        with open('fb_tree.json', 'w') as f:
                json_data = json.dumps(test, indent=4)
                f.write(json_data)
    else:
        print(f'else{fb_json}')
    
    return fb_json
    
    
        


async def main():
    start = time.time()

    await process_fb()

    end = time.time()
    total_time = end - start
    print(f"Código finalizado em {total_time} secs")

asyncio.run(main())
