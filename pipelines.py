# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import csv
from scrapy.pipelines.images import ImagesPipeline


class DcunsplashPipeline:
    def process_item(self, item, spider):
        return item


class UnsplashImagesPipeline(ImagesPipeline):
    def __init__(self, store_uri, download_func=None, settings=None):
        super().__init__(store_uri, download_func, settings)
        self.fieldnames = ['category', 'title', 'url', 'path']
        with open('photos.csv', 'a') as csvfile:
            csvwriter = csv.DictWriter(csvfile, fieldnames=self.fieldnames, delimiter=';')
            csvwriter.writeheader()

    def get_media_requests(self, item, info):
        if item['url']:
            urls = item['url'].split(',')
            try:
                yield scrapy.Request(urls[0])
            except Exception as e:
                print(e)

    def item_completed(self, results, item, info):
        if results:
            data = {'category': item['category'][0], 'title': item['title'][0], 'path': results[0][1]['path'], 'url': results[0][1]['url']}
            with open('photos.csv', 'a') as csvfile:
                csvwriter = csv.DictWriter(csvfile, fieldnames=self.fieldnames, delimiter=';')
                csvwriter.writerow(data)
