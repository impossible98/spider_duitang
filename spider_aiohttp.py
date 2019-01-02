import json
import os
import time
from hashlib import md5
import asyncio

import aiofiles
import aiohttp
import json_aiohttp

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DIST_DIR = os.path.join(BASE_DIR, 'dist')


class Spider(json_aiohttp.Spider):
    def __init__(self, kw, start=0):
        self.kw = kw
        self.start = start

    async def test(self, response):
        response = await Spider.get_html(self)
        result = json.loads(response)
        data = result.get('data')
        if data:
            object_list = data.get('object_list')
            if not object_list:
                pass
            else:
                for i in object_list:
                    items = {}
                    photo = i.get('photo')
                    if photo:
                        path = photo.get('path')
                        if path:
                            items['path'] = path
                    yield items

    async def get_html_2(self, item):
        item = await Spider.test(self, response)
        try:
            url = item.get('path')
            headers = {
                'User-Agent':
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
            if 'gif_jpeg' in url:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url[:-5], headers=headers) as response:
                        if response.status == 200:
                            return await ('gif', response.read())
            elif 'png' in url:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, headers=headers) as response:
                        if response.status == 200:
                            return await ('png', response.read())
            elif 'jpg' or 'jpeg' in url:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, headers=headers) as response:
                        if response.status == 200:
                            return await ('jpg', response.read())
            else:
                print('Unknown format.')
                pass
        except aiohttp.ClientConnectionError as e:
            print(e)
            pass

    async def write_into_file(self, format, response2):
        format, response2 = await Spider.get_html_2(self, item)
        if not os.path.exists(os.path.join(DIST_DIR, self.kw)):
            os.makedirs(os.path.join(DIST_DIR, self.kw))
        if format == 'gif':
            file_path = '{0}/{1}/{2}.{3}'.format(
                DIST_DIR, self.kw,
                md5(response2.content).hexdigest(), 'gif')
            if not os.path.exists(file_path):
                with open(file_path, 'wb') as f:
                    f.write(response2.content)
            else:
                print('Already Downloaded {0}.gif'.format(
                    md5(response2.content).hexdigest()))
        elif format == 'png':
            file_path = '{0}/{1}/{2}.{3}'.format(
                DIST_DIR, self.kw,
                md5(response2.content).hexdigest(), 'png')
            if not os.path.exists(file_path):
                with open(file_path, 'wb') as f:
                    f.write(response2.content)
            else:
                print('Already Downloaded {0}.png'.format(
                    md5(response2.content).hexdigest()))
        elif format == 'jpg':
            file_path = '{0}/{1}/{2}.{3}'.format(
                DIST_DIR, self.kw,
                md5(response2.content).hexdigest(), 'jpg')
            if not os.path.exists(file_path):
                with open(file_path, 'wb') as f:
                    f.write(response2.content)
            else:
                print('Already Downloaded {0}.jpg'.format(
                    md5(response2.content).hexdigest()))


def main():
    # print('Enter the keyowrd: ', end='')
    # kw = input()
    kw = 'taeyeon'
    start = time.time()
    counter = 0
    tasks = [asyncio.Semaphore(500)]
    loop = asyncio.get_event_loop()
    for i in range(0, 96, 24):
        spider = Spider(kw, start=i)
        response = spider.get_html()
        tasks.append(response)
        items = spider.test(response)
        tasks.append(items)
        if items:
            for item in items:
                format, response = spider.get_html_2(item)
                tasks.append((format, response))
                if format == 'gif':
                    print('Downloading: {0} It costs {1}s.'.format(
                        item['path'][:-5], time.time() - start))
                else:
                    print('Downloading: {0} It costs {1}s.'.format(
                        item['path'], time.time() - start))
                counter += 1
                tasks.append(spider.write_into_file(format, response))
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
    print('Get {0}. It costs {1}s'.format(counter, str(time.time() - start)))


if __name__ == '__main__':
    main()
