from clickhouse_driver import Client
import json

# Загрузите данные в ClickHouse и создайте таблицу для их хранения.

client = Client('localhost')

client.execute('CREATE DATABASE IF NOT EXISTS books')

client.execute('''
CREATE TABLE IF NOT EXISTS books.catalog (
    id Int,
    title String,
    price String,
    desc String,
    in_stock Int,
) ENGINE = MergeTree()
ORDER BY id
''')

print("Таблица создана успешно.")

with open('books.json', 'r') as file:
    data = json.load(file)
n = 1
for book in data:
    client.execute("""
    INSERT INTO books.catalog (
        id, title, price,
        desc, in_stock
    ) VALUES""",
    [(n,
      book['title'] or "",
      book['price'] or "",
      book['desc'] or "",
      book['in_stock'] or "")])
    n += 1

print("Данные введены успешно.")

result = client.execute("SELECT * FROM books.catalog")
print("Вставленная запись:", result[0])
