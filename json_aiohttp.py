import asyncio
import json
import os
import time

import aiofiles
import aiohttp

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DIST_DIR = os.path.join(BASE_DIR, 'dist')


class Spider:
    def __init__(self, kw, start=0):
        self.kw = kw
        self.start = start

    async def get_html(self):
        url = 'https://www.duitang.com/napi/blog/list/by_search/?kw={0}&type=feed&include_fields=top_comments%2Cis_root%2Csource_link%2Citem%2Cbuyable%2Croot_id%2Cstatus%2Clike_count%2Clike_id%2Csender%2Calbum%2Creply_count%2Cfavorite_blog_id&_type=&start={1}'.format(
            self.kw, self.start)
        headers = {
            'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
        }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        return await response.text()
        except aiohttp.ClientConnectionError as e:
            print(e)
            pass

    async def test(self, response):
        response = await Spider.get_html(self)
        result = json.loads(response)
        data = result.get('data')
        if data:
            object_list = data.get('object_list')
            if not object_list:
                return None
            else:
                return True

    async def write_into_file(self, response):
        response = await Spider.get_html(self)
        result = json.dumps(json.loads(response),
                            indent=4, ensure_ascii=False)
        if not os.path.exists(
                os.path.join(os.path.join(DIST_DIR, 'json'), self.kw)):
            os.makedirs(os.path.join(os.path.join(DIST_DIR, 'json'), self.kw))
        async with aiofiles.open(
                'dist/json/{0}/{1}.json'.format(self.kw,
                                                int(self.start / 24) + 1),
                'w',
                encoding='utf-8') as f:
            await f.write(result)


def main():
    # print('Enter the keyowrd: ', end='')
    # kw = input()
    kw = 'taeyeon'
    start = time.time()
    counter = 0
    tasks = [asyncio.Semaphore(500)]
    loop = asyncio.get_event_loop()
    for i in range(0, 240, 24):
        spider = Spider(kw, start=i)
        response = spider.get_html()
        tasks.append(response)
        items = spider.test(response)
        tasks.append(items)
        if items:
            print(
                'Downloading: {0}.json It costs {1}s'.format(
                    str(i // 24 + 1), str(time.time() - start)),)
            tasks.append(spider.write_into_file(response))
            counter += 1
        else:
            break
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
    print('Get {0}. It costs {1}s'.format(counter, str(time.time() - start)))


if __name__ == '__main__':
    main()
