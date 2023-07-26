from database.connector import Connector
from alive_progress import alive_it
from view.view import View
import time


class Migration(Connector):
    _tables: list[str] = ['store', 'category', 'product']

    def run(self):
        for table_name in alive_it(self._tables):
            print('Create table -> %s%s%s' % (View.COLOR_L_GREEN, table_name, View.COLOR_DEFAULT))
            file = open('./migration/%s_table.db' % table_name, 'r')
            query: str = file.read()
            super().get_cursor().execute(query)
            time.sleep(0.3)
