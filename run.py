import requests
import os
from dotenv import load_dotenv
import sys
from view.view import View

load_dotenv()

view = View()
view.separator()
view.showBanner()
view.separator()
view.showMenu()
view.separator()
menuNumber: str = view.proposeChoose()

print(menuNumber)

exit()

response = requests.get('https://stores-api.zakaz.ua/stores')
data = response.json()

print(data)
