"""
    Найдите сайт, содержащий интересующий вас список или каталог. Это может быть список книг, фильмов,
    спортивных команд или что-то еще, что вас заинтересовало.
    Создайте новый проект Scrapy и определите нового паука.
    С помощью атрибута start_urls укажите URL выбранной вами веб-страницы.
    Определите метод парсинга для извлечения интересующих вас данных.
    Используйте селекторы XPath или CSS для навигации по HTML и извлечения данных.
    Возможно, потребуется извлечь данные с нескольких страниц или перейти по ссылкам на другие страницы.
    Сохраните извлеченные данные в структурированном формате.
    Вы можете использовать оператор yield для возврата данных из паука, которые Scrapy может записать
    в файл в выбранном вами формате (например, JSON или CSV).
    Конечным результатом работы должен быть код Scrapy Spider, а также пример выходных данных.
    Не забывайте соблюдать правила robots.txt и условия обслуживания веб-сайта,
    а также ответственно подходите к использованию веб-скрейпинга.
"""

from scrapy.crawler import CrawlerProcess
from scrapy.utils.reactor import install_reactor
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

from DCConverters.spiders.chipdipru import ChipdipruSpider

if __name__ == "__main__":
    configure_logging()
    install_reactor('twisted.internet.asyncioreactor.AsyncioSelectorReactor')
    process = CrawlerProcess(get_project_settings())
    process.crawl(ChipdipruSpider)
    process.start()
