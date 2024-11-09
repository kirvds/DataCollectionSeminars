import requests as req
import json
import re
from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent
ua = UserAgent()

# название, цену, количество товара в наличии (In stock (19 available)) в формате integer, описание.

url = 'http://books.toscrape.com/catalogue/'
url_page = 'http://books.toscrape.com/catalogue/page-'
headers = {'User-Agent': ua.chrome}
params = {'ref_': 'bo_nb_hm_tab'}

session = req.session()

books = []
page_n = 1
while True:
    response = session.get(url_page+str(page_n)+'.html', headers=headers)
    if response.status_code != 200:
        print(f"Код: {response.status_code}")
        break

    soup = bs(response.text, "html.parser")
    posts = soup.find_all('article', {'class': 'product_pod'})
    for post in posts:
        post_info = {}

        name_info = post.find('h3')
        post_info['title'] = name_info.getText()
        price_info = post.find('p', {'class': 'price_color'})
        post_info['price'] = price_info.getText()
        url_desc = url + name_info.find('a').get('href')

        response = session.get(url_desc, headers=headers)
        soup = bs(response.text, "html.parser")
        article = soup.find('article', {'class': 'product_page'})
        desc_info = article.find('p', {'class': ''})
        if desc_info:
            post_info['desc'] = desc_info.getText()
        else:
            post_info['desc'] = None
        in_stock = article.find('p', {'class': 'instock availability'})
        post_info['in_stock'] = int(re.findall(r'\d+', in_stock.getText())[0])

        books.append(post_info)

    print(f"Обработана страница {page_n}")
    page_n += 1

print(f"{len(books)} книг")
# json_str = json.dumps(books)
# print(type(json_str))
# print("Json List:", json_str)

with open("books.json", "w") as final:
    json.dump(books, final)
