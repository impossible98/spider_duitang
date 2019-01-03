import json
import os
import time
from hashlib import md5

import requests

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DIST_DIR = os.path.join(BASE_DIR, 'dist')


class Spider:
    def __init__(self, kw, start=0):
        self.kw = kw
        self.start = start

    def get_html(self):
        url = 'https://www.duitang.com/napi/blog/list/by_search/?kw={0}&type=feed&include_fields=top_comments%2Cis_root%2Csource_link%2Citem%2Cbuyable%2Croot_id%2Cstatus%2Clike_count%2Clike_id%2Csender%2Calbum%2Creply_count%2Cfavorite_blog_id&_type=&start={1}'.format(
            self.kw, self.start)
        headers = {
            'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
        }
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return response.text
        except requests.ConnectionError as e:
            print(e)
            pass

    def test(self, response):
        result = json.loads(response)
        data = result.get('data')
        if data:
            object_list = data.get('object_list')
            if not object_list:
                return None
            else:
                for i in object_list:
                    items = {}
                    photo = i.get('photo')
                    if photo:
                        path = photo.get('path')
                        if path:
                            items['path'] = path
                    yield items

    def get_html_2(self, item):
        try:
            url = item.get('path')
            headers = {
                'User-Agent':
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
            }
            if 'gif_jpeg' in url:
                response = requests.get(url[:-5], headers=headers)
                if response.status_code == 200:
                    return ('gif', response)
            elif 'png' in url:
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    return ('png', response)
            elif 'jpg' or 'jpeg' in url:
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    return ('jpg', response)
            else:
                print('Unknown format.')
                pass
        except requests.ConnectionError as e:
            print(e)
            pass

    def write_into_file(self, format, response):
        if not os.path.exists(os.path.join(DIST_DIR, self.kw)):
            os.makedirs(os.path.join(DIST_DIR, self.kw))
        if format == 'gif':
            file_path = '{0}/{1}/{2}.{3}'.format(
                DIST_DIR, self.kw,
                md5(response.content).hexdigest(), 'gif')
            if not os.path.exists(file_path):
                with open(file_path, 'wb') as f:
                    f.write(response.content)
            else:
                print('Already Downloaded {0}.gif'.format(
                    md5(response.content).hexdigest()))
        elif format == 'png':
            file_path = '{0}/{1}/{2}.{3}'.format(
                DIST_DIR, self.kw,
                md5(response.content).hexdigest(), 'png')
            if not os.path.exists(file_path):
                with open(file_path, 'wb') as f:
                    f.write(response.content)
            else:
                print('Already Downloaded {0}.png'.format(
                    md5(response.content).hexdigest()))
        elif format == 'jpg':
            file_path = '{0}/{1}/{2}.{3}'.format(
                DIST_DIR, self.kw,
                md5(response.content).hexdigest(), 'jpg')
            if not os.path.exists(file_path):
                with open(file_path, 'wb') as f:
                    f.write(response.content)
            else:
                print('Already Downloaded {0}.jpg'.format(
                    md5(response.content).hexdigest()))


def main():
    # print('Enter the keyowrd: ', end='')
    # kw = input()
    kw = 'correct'
    start = time.time()
    counter = 0
    for i in range(0, 3600, 24):
        spider = Spider(kw, start=i)
        response = spider.get_html()
        items = spider.test(response)
        if items:
            for item in items:
                format, response = spider.get_html_2(item)
                if format == 'gif':
                    print('Downloading: {0} It costs {1}s.'.format(
                        item['path'][:-5], time.time() - start))
                else:
                    print('Downloading: {0} It costs {1}s.'.format(
                        item['path'], time.time() - start))
                counter += 1
                spider.write_into_file(format, response)
        else:
            break
    print('Get {0}. It costs {1}s'.format(counter, str(time.time() - start)))


if __name__ == '__main__':
    main()
