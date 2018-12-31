import json
import os
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
            return None

    def test(self, text):
        result = json.loads(text)
        data = result.get('data')
        if data:
            object_list = data.get('object_list')
            if not object_list:
                return []
            else:
                for item in object_list:
                    contents = {}
                    contents['path'] = item.get('photo').get('path')
                    yield contents

    def write_into_file(self, item):
        if not os.path.exists(os.path.join(DIST_DIR, self.kw)):
            os.makedirs(os.path.join(DIST_DIR, self.kw))
        try:
            image_url = item.get('path')
            if 'gif' in image_url:
                response = requests.get(image_url)
                if response.status_code == 200:
                    file_path = '{0}/{1}/{2}.{3}'.format(
                        DIST_DIR, self.kw,
                        md5(response.content).hexdigest(), 'gif')
                    if not os.path.exists(file_path):
                        with open(file_path, 'wb') as f:
                            f.write(response.content)
                    else:
                        print(
                            'Already Downloaded',
                            md5(response.content).hexdigest(),
                            'gif',
                            sep='')
            else:
                response = requests.get(image_url)
                if response.status_code == 200:
                    file_path = '{0}/{1}/{2}.{3}'.format(
                        DIST_DIR, self.kw,
                        md5(response.content).hexdigest(), 'jpg')
                    if not os.path.exists(file_path):
                        with open(file_path, 'wb') as f:
                            f.write(response.content)
                    else:
                        print(
                            'Already Downloaded',
                            md5(response.content).hexdigest(),
                            'jpg',
                            sep='')
        except requests.ConnectionError:
            print('Failed to save image')


def main():
    kw = 'taeyeon'
    for i in range(0, 3600, 24):
        spider = Spider(kw, start=i)
        text = spider.get_html()
        items = spider.test(text)
        if items:
            for item in items:
                if 'gif' in item.get('path'):
                    print('Downloading: ' + item['path'][:-5])
                else:
                    print('Downloading: ' + item['path'])
                spider.write_into_file(item)


if __name__ == '__main__':
    main()