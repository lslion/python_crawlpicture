# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy.http import Request
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

class PythonCrawlpicturePipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        # id = re.findall('http://724.169pp.net/bizhi/(.*?).jpg', request.url)[0]
        id = request.url[(request.url.find('/', 7) + 1):]
        id = id.replace('/', '_')
        print('image name is: ' + id)
        return 'full/%s' % (id)

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            print('img addr is: ' + image_url)
            referer = item['referer_url']
            yield Request(image_url, headers={'Referer':referer})

    def item_completed(self, results, item, info):
        image_path = [x['path'] for ok, x in results if ok]
        if not image_path:
            print('Item contains no images')
            raise DropItem('Item contains no images')
        item['image_paths'] = image_path
        return item
