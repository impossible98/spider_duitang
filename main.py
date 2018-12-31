import json
import os
from hashlib import md5
from multiprocessing.dummy import Pool

import requests

# 参数
GROUP_START = 1
GROUP_END = 10
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DIST_DIR = os.path.join(BASE_DIR, "dist")


def get_html(kw, start):
    """获取网页源代码

    """
    url = "https://www.duitang.com/napi/blog/list/by_search/?kw={}&start={}".format(kw, start)
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            result = response.json()
            return result
    except requests.ConnectionError as e:
        print(e)
        return None


def get_images(json):
    """获取image的url

    """
    data = json.get("data")
    if data:
        object_list = data.get("object_list")
        if object_list:
            for item in object_list:
                contents = {}
                contents["path"] = item.get("photo").get("path")
                yield contents


def write_into_file(keyword, item):
    """写入文件

    """
    if not os.path.exists(os.path.join(DIST_DIR, keyword)):
        os.makedirs(os.path.join(DIST_DIR, keyword))
    try:
        image_url = item.get("path")
        if "gif" in image_url:
            response = requests.get(image_url)
            if response.status_code == 200:
                file_path = "{0}/{1}/{2}.{3}".format(DIST_DIR, keyword,
                                                     md5(response.content).hexdigest(), "gif")
                if not os.path.exists(file_path):
                    with open(file_path, "wb") as f:
                        f.write(response.content)
                else:
                    print("Already Downloaded", md5(
                        response.content).hexdigest(), "gif", sep="")
        else:
            response = requests.get(image_url)
            if response.status_code == 200:
                file_path = "{0}/{1}/{2}.{3}".format(DIST_DIR, keyword,
                                                     md5(response.content).hexdigest(), "jpg")
                if not os.path.exists(file_path):
                    with open(file_path, "wb") as f:
                        f.write(response.content)
                else:
                    print("Already Downloaded", md5(
                        response.content).hexdigest(), "jpg", sep="")
    except requests.ConnectionError:
        print("Failed to save image")


def main(start):
    """主函数

    """
    # 这里修改kw
    kw = "泰妍"
    json = get_html(kw, start)
    for item in get_images(json):
        print("正在下载: ", item["path"], sep="")
        write_into_file(kw, item)


if __name__ == '__main__':
    pool = Pool(16)
    groups = ([x * 24 for x in range(GROUP_START-1, GROUP_END+1)])
    pool.map(main, groups)
    pool.close()
    pool.join()