# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from hashlib import md5

import scrapy
from scrapy.pipelines.images import ImagesPipeline


class SpiderScrapyPipeline:
    def __init__(self):
        pass


class ImagePipeline(ImagesPipeline):
    def file_path(self, request, item, response=None, info=None):
        if 'gif' in item['path']:
            filename = '{1}.{2}'.format(
                md5(response.content).hexdigest(), 'gif')
        elif 'png' in item['path']:
            filename = '{1}.{2}'.format(
                md5(response.content).hexdigest(), 'png')
        elif 'jpg' or 'jpeg' in item['path']:
            filename = '{1}.{2}'.format(
                md5(response.content).hexdigest(), 'jpg')
        return filename

    def get_media_requests(self, item, info):
        yield scrapy.Request(item['path'])
