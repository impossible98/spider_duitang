# -*- coding: utf-8 -*-
import scrapy
import json
import os
import sys
import time
from spider_scrapy.items import SpiderScrapyItem


class DuitangSpider(scrapy.Spider):
    name = 'duitang'
    allowed_domains = ['duitang.com']
    kw = 'correct'
    # start_urls = []

    def start_requests(self):
        for start in range(0, 360, 24):
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
                for i in object_list:
                    item = SpiderScrapyItem()
                    photo = i.get('photo')
                    if photo:
                        path = photo.get('path')
                        if path:
                            if 'gif_jpeg' in path:
                                item['path'] = path[:-5]
                            else:
                                item['path'] = path
                    yield item
