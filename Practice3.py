import json
from pymongo import MongoClient

# Загрузите данные который вы получили на предыдущем уроке путем скрейпинга сайта с помощью Buautiful Soup в MongoDB
# и создайте базу данных и коллекции для их хранения.
# Поэкспериментируйте с различными методами запросов.

client = MongoClient('mongodb://localhost:27017/')

db = client['books']
# db.catalog.drop()
# db.catalog.delete_many({})

collection = db['catalog']

# with open("books.json", "r") as f:
#     catalog = json.load(f)
#
# # collection.insert_many(catalog)
# n = 0
# for book in catalog:
#     book['_id'] = n
#     collection.insert_one(book)
#     n += 1
#
# print("Каталог успешно внесен")

# for book in collection.find({'in_stock': {'$gt': 19}}):
#     print(book.get('title'))

for book in collection.find({'$or': [{'in_stock': 22}, {'title': {'$regex': 'Art'}}]}):
    print(book.get('title'), book.get('in_stock'), 'шт.')
