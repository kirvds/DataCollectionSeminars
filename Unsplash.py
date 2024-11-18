import scrapy
from scrapy.http import HtmlResponse
from DCUnsplash.items import DcunsplashItem
from scrapy.loader import ItemLoader

class UnsplashSpider(scrapy.Spider):
    name = "Unsplash"
    allowed_domains = ["unsplash.com"]
    start_urls = ["https://unsplash.com"]

    def parse(self, response: HtmlResponse):
        categories = response.xpath("//div[@class='qaAX1']//a[contains(@class, 'wuIW2 R6ToQ')]")
        for category in categories:
            yield response.follow(category, callback=self.parse_category)

    def parse_category(self, response: HtmlResponse):
        cat_title = response.xpath('//h1/text()').get()
        items = response.xpath('//figure[@data-testid="photo-grid-masonry-figure"]//a[@itemprop="contentUrl"]')
        for item in items:
            yield response.follow(item, callback=self.parse_image,
                                  cb_kwargs={'category': cat_title, 'title': item.xpath('.//@title').get()})

    def parse_image(self, response: HtmlResponse, category, title):
        loader = ItemLoader(item=DcunsplashItem(), response=response)
        loader.add_value('category', category)
        loader.add_value('title', title)
        loader.add_xpath('url', "//div[@class='Tbd2Y']//img[contains(@srcset, 'https')]/@srcset")

        yield loader.load_item()
