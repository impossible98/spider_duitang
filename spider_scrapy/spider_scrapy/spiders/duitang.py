# -*- coding: utf-8 -*-
import scrapy
import json
import os
import sys
import time
from spider_scrapy.items import SpiderScrapyItem

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DIST_DIR = os.path.join(BASE_DIR, 'dist')


class DuitangSpider(scrapy.Spider):
    name = 'duitang'
    allowed_domains = ['duitang.com']
    kw = 'correct'
    # start_urls = []

    def start_requests(self):
        for start in range(0, 1200, 24):
            url = 'https://www.duitang.com/napi/blog/list/by_search/?kw={0}&type=feed&include_fields=top_comments%2Cis_root%2Csource_link%2Citem%2Cbuyable%2Croot_id%2Cstatus%2Clike_count%2Clike_id%2Csender%2Calbum%2Creply_count%2Cfavorite_blog_id&_type=&start={1}'.format(
                self.kw, start)

            # url = 'https://www.duitang.com/napi/blog/list/by_search/?kw=correct&type=feed&include_fields=top_comments%2Cis_root%2Csource_link%2Citem%2Cbuyable%2Croot_id%2Cstatus%2Clike_count%2Clike_id%2Csender%2Calbum%2Creply_count%2Cfavorite_blog_id&_type=&start=48'
            yield scrapy.Request(url, self.parse)

    def parse(self, response):
        item = SpiderScrapyItem()
        result = json.loads(response.text)
        data = result.get('data')
        if data:
            object_list = data.get('object_list')
            if object_list:
                result = json.dumps(json.loads(response.text),
                                    indent=4, ensure_ascii=False)
                result_dir = os.path.join(
                    os.path.join(DIST_DIR, 'json'), self.kw)
                page = response.url.split("=")[-1]
                if not os.path.exists(result_dir):
                    os.makedirs(result_dir)
                result_path = os.path.join(
                    result_dir, '{0}.json'.format(int(page) // 24 + 1))
                item['result'] = result
                return item

            else:
                pass

