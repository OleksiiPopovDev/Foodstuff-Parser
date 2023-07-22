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
view.separator()
exit()
response = requests.get('%s/stores' % os.getenv('SOURCE_URL'))
data = response.json()

print(data)
