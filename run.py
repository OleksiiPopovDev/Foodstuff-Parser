import requests
import os
from dotenv import load_dotenv
import sys
from view.view import View

load_dotenv()

view = View([
    'Run parser from start',
    'Run parser from last stopped point',
    'Refresh database'
])

print(view.selectedMenu)
view.separator()
exit()
response = requests.get('%s/stores' % os.getenv('SOURCE_URL'))
data = response.json()

print(data)
