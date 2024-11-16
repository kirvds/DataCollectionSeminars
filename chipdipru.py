import scrapy
from scrapy.http import HtmlResponse
from DCConverters.items import DcconvertersItem

class ChipdipruSpider(scrapy.Spider):
    name = "chipdipru"
    allowed_domains = ["chipdip.ru"]
    start_urls = ["https://www.chipdip.ru/catalog/ic-dc-dc-converters?ps=x3"]

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//li[@class='pager__page']/a[contains(@class, 'pager__next')]/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        items = response.xpath("//tr[@class='with-hover' and contains(@id, 'item')]")
        for item in items:
            name = item.xpath(".//a[@class='link']/text()").get()
            url = item.xpath(".//a[@class='link']/@href").get()
            brand = item.xpath(".//div[@class='nw']/span/text()").get()
            availability = item.xpath(".//span[contains(@class, 'item__avail')]")
            price = item.xpath(".//span[contains(@id, 'price')]/text()").get()
            yield DcconvertersItem(name=name, url=url, brand=brand, availability=availability, price=price)
