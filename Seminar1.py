import os.path
import sys
import requests as req
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

url = 'https://api.foursquare.com/v3/places/search'
header = 'accept: application/json'

params = {
    'fields': 'name,location,rating'
    # 'query': 'coffee',
    # 'll': "59.93,30.31",
    # 'radius': "1000",
    # 'll': '13032,13033,13034,13035'
}

headers = {
    'accept': 'application/json',
    'Authorization': os.getenv('API_KEY')
}

near = input("Введите город: ")
params['near'] = near
сtype = input("Введите категорию заведения: ")
if сtype == "":
    catid = input("Введите индекс категории заведения: ")
    if catid is not None:
        params['categories'] = catid
    else:
        sys.exit()
else:
    params['query'] = сtype

response = req.get(url, params=params, headers=headers)
j_data = response.json()

if j_data.get('results') is None:
    print("Нет данных")
else:
    for res in j_data.get('results'):
        print(f"Название: \"{res.get('name')}\", адрес: {res.get('location').get('formatted_address')}, рейтинг: {res.get('rating')}")
