# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import csv

class DcconvertersPipeline:
    def __init__(self):
        self.fieldnames = ['name', 'url', 'brand', 'availability', 'price']
        with open('chipdipru.csv', 'a') as csvfile:
            csvwriter = csv.DictWriter(csvfile, fieldnames=self.fieldnames, delimiter=';')
            csvwriter.writeheader()

    def process_item(self, item, spider):
        av = item.get('availability')
        no = av.xpath("./text()").get()
        if no is None:
            item['availability'] = 'no'
        else:
            txt = av.xpath(".//span[@class='nw']/text()").getall()
            item['availability'] = txt[0] + txt[1]

        item['price'] = item.get('price').replace('\xa0', '')
        with open(spider.name + '.csv', 'a') as csvfile:
            csvwriter = csv.DictWriter(csvfile, fieldnames=self.fieldnames, delimiter=';')
            csvwriter.writerow(item)

        return item
