import json
import os

import requests

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DIST_DIR = os.path.join(BASE_DIR, "dist")


def get_html(kw, start):
    """获取网页源代码

    """
    url = "https://www.duitang.com/napi/blog/list/by_search/?kw={}&start={}"
    new_url = url.format(kw, start)
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
    }
    try:
        response = requests.get(new_url, headers=headers)
        if response.status_code == 200:
            result = json.dumps(response.json(), indent=4, ensure_ascii=False)
            return result
    except requests.ConnectionError as e:
        print(e)
        return None


def write_into_file(result):
    """写入文件

    """
    if not os.path.exists(DIST_DIR):
        os.makedirs(DIST_DIR)
    with open("dist/result.json", "w", encoding="utf-8") as f:
        f.write(result)


def main():
    """主函数

    """
    # 可以修改的测试值 start=24
    kw = "taeyeon"
    start = 0
    result = get_html(kw, start)
    write_into_file(result)


if __name__ == "__main__":
    main()