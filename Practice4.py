from lxml import html
import requests as req
import csv
from pprint import pprint

# Выберите веб-сайт с табличными данными, который вас интересует.
# Напишите код Python, использующий библиотеку requests для отправки HTTP GET-запроса на сайт
# и получения HTML-содержимого страницы.
# Выполните парсинг содержимого HTML с помощью библиотеки lxml, чтобы извлечь данные из таблицы.
# Сохраните извлеченные данные в CSV-файл с помощью модуля csv.
#
# Ваш код должен включать следующее:
#
# Строку агента пользователя в заголовке HTTP-запроса, чтобы имитировать веб-браузер и избежать блокировки сервером.
# Выражения XPath для выбора элементов данных таблицы и извлечения их содержимого.
# Обработка ошибок для случаев, когда данные не имеют ожидаемого формата.
# Комментарии для объяснения цели и логики кода.


url = 'https://predictorllc.ru/catalog/shagovye-dvigateli/nema23/'
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'}


# функция
def is_float(element: any) -> bool:
    """Функция проверки строки на принадлежность к числам.
    Возвращает логическое значение и само число с плавающей запятой в случае успешного преобразования."""
    if element is None:
        return False, 0.
    try:
        fval = float(element.replace(',', '.'))
        return True, fval
    except ValueError:
        return False, 0.


session = req.session()
response = session.get(url, headers=headers)  # запрос страницы
dom = html.fromstring(response.text)  # преобразование html в дерево элементов
steppers = []

rows = dom.xpath("//table[contains(@class, 'table')]//tr")  # выделение списка строк таблицы

cols_not2read = [1, 10, 11]  # указанные столбцы отсутствуют в строке заголовков, а в остальных не отфильтровываются другим способом
# вообще почему-то row.xpath(".//td/text()") выдает неожиданные столбцы, которые не наблюдаются в html
first_row = True
for row in rows:  # цикл по строкам таблицы
    item_info = []
    conlumns = row.xpath(".//td/text()")
    first = True
    ncol = 0
    for col in conlumns:  # цикл по столбцам таблицы
        if first and not first_row:  # строка заголовков отличается
            try:
                strng = str(row.xpath(".//td/a/text()")[0]).strip()  # xpath выделит первый и последний столбец. Последний не нужен.
            except:
                strng = ""
            first = False
        else:
            strng = str(col).strip()
        is_fval, fval = is_float(strng)
        if not first_row and is_fval:
            item_info.append(fval)
        else:
            if first_row or ncol not in cols_not2read:
                item_info.append(strng)
        ncol += 1

    if first_row and len(item_info) > 9:
        item_info.remove(item_info[-1])
    first_row = False
    steppers.append(item_info)

# pprint(items_list)
with open('steppers.csv', 'w') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=';')
    csvwriter.writerows(steppers)


