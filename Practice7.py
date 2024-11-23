"""
    Выберите веб-сайт, который содержит информацию, представляющую интерес для извлечения данных.
    Это может быть новостной сайт, платформа для электронной коммерции или любой другой сайт,
    который позволяет осуществлять скрейпинг (убедитесь в соблюдении условий обслуживания сайта).
    Используя Selenium, напишите сценарий для автоматизации процесса перехода на нужную страницу сайта.
    Определите элементы HTML, содержащие информацию, которую вы хотите извлечь
    (например, заголовки статей, названия продуктов, цены и т.д.).
    Используйте BeautifulSoup для парсинга содержимого HTML и извлечения нужной информации из идентифицированных элементов.
    Обработайте любые ошибки или исключения, которые могут возникнуть в процессе скрейпинга.
    Протестируйте свой скрипт на различных сценариях, чтобы убедиться, что он точно извлекает нужные данные.
    Предоставьте ваш Python-скрипт вместе с кратким отчетом (не более 1 страницы), который включает следующее:
    URL сайта. Укажите URL сайта, который вы выбрали для анализа. Описание. Предоставьте краткое описание информации,
    которую вы хотели извлечь из сайта. Подход.
    Объясните подход, который вы использовали для навигации по сайту, определения соответствующих элементов
    и извлечения нужных данных. Трудности.
    Опишите все проблемы и препятствия, с которыми вы столкнулись в ходе реализации проекта, и как вы их преодолели.
    Результаты. Включите образец извлеченных данных в выбранном вами структурированном формате (например, CSV или JSON).
"""
import csv
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

options = Options()
options.add_argument('start-maximized')
driver = webdriver.Chrome(options=options)

driver.get('https://youla.ru/sankt-peterburg')

input = driver.find_element(by=By.ID, value='downshift-0-input')
input.send_keys("ноутбуки")
input.send_keys(Keys.ENTER)

wait = WebDriverWait(driver, 30)
lines = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@data-test-component="ProductOrAdCard"]')))
lines = []
data = []
while True:
    count = len(lines)
    print(count)
    driver.execute_script('window.scrollBy(0,5000)')
    time.sleep(5)
    lines = driver.find_elements(by=By.XPATH, value='//div[@class="sc-gIvKln gTlSZy"]')
    for line in lines:
        cards = line.find_elements(by=By.XPATH, value='.//div[@data-test-component="ProductOrAdCard"]')
        for card in cards:
            try:
                title = card.find_element(by=By.XPATH, value='.//span[@data-test-block="ProductName"]').text
                is_included = False
                for d in data:
                    if d['title'] == title:
                        is_included = True
                        break
                if is_included or title == '':
                    continue
                price = card.find_element(by=By.XPATH, value='.//span[@data-test-component="Price"]').text.replace('\u205f', '')
                url = card.find_element(by=By.XPATH, value='.//a').get_attribute('href')

                data.append({'title': title, 'price': price, 'url': url})
            except:
                pass
    if len(lines) == count:
        break


# soup = BeautifulSoup(driver.page_source, 'html.parser')

print()
driver.quit()

fieldnames = ['title', 'price', 'url']
with open('notebooks.csv', 'a') as csvfile:
    csvwriter = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
    csvwriter.writerows(data)
