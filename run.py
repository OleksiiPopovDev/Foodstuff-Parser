from dotenv import load_dotenv
from view.view import View
from database.migration_mysql import MigrationMySQL
from service.store_parser import StoreParser
from service.category_parser import CategoryParser
from service.product_parser import ProductParser

load_dotenv()

view = View([
    'Run parser from scratch (Refresh Database)',
    'Base Parsing',
    'Continue Parsing',
])

while view.selected_menu != 0:
    view.separator()

    if view.selected_menu == 1:
        migration = MigrationMySQL()
        migration.run()
        view.separator()

        view.show_menu()

    elif view.selected_menu == 2:
        store = StoreParser()
        store.run()
        view.separator()

        category = CategoryParser()
        category.run()
        view.separator()

        view.show_menu()

    elif view.selected_menu == 3:
        product = ProductParser()
        product.run()
        view.separator()

        view.show_menu()
