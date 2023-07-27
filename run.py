from dotenv import load_dotenv
import sys
from view.view import View
from database.migration import Migration
from service.store_parser import StoreParser
from service.category_parser import CategoryParser

load_dotenv()

view = View([
    'Exit',
    'Run Migration',
    'Run parser from last stopped point',
])

while view.selected_menu != 0:
    view.separator()

    if view.selected_menu == 1:
        migration = Migration()
        migration.run()
        view.separator()
        view.show_menu()
    elif view.selected_menu == 2:
        #store = StoreParser()
        #store.run()
        category = CategoryParser()
        category.run()
        view.separator()
        view.show_menu()
