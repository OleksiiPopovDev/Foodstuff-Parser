import requests

response = requests.get('https://stores-api.zakaz.ua/stores')
data = response.json()

print(data)