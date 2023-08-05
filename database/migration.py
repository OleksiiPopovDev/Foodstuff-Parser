from database.connector import Connector
from alive_progress import alive_bar
from view.view import View
import time
import os


class Migration(Connector):
    _dump_directory: str = 'database/dumps/'
    _tables: list[str] = ['store', 'category', 'product', 'product_detail', 'statistic']

    def run(self):
        if not os.path.exists(self._dump_directory):
            os.makedirs(self._dump_directory)

        db_file: str = 'database/%s.db' % os.getenv('DB_FILE_NAME')
        if os.path.isfile(db_file):
            os.rename(db_file, 'database/dumps/%s_%s.db' % (os.getenv('DB_FILE_NAME'), time.time()))
            self.create_connection()

        with alive_bar(len(self._tables)) as bar:
            biggest_table_name: int = View.count_biggest_line(self._tables)

            for table_name in self._tables:
                count_spaces = View.get_count_spaces_for_line_up(table_name, biggest_table_name)
                bar.title(
                    View.paint('\t\t{Yellow}Creating table{ColorOff} -> {BYellow}%s{ColorOff}' % table_name) +
                    (' ' * count_spaces)
                )

                file = open('./migration/%s_table.db' % table_name, 'r')
                query: str = file.read()
                super().get_cursor().execute(query)
                super().commit()
                file.close()

                print(View.paint(
                    '\t\t{Yellow}Created table {ColorOff} >> {BGreen}%s{ColorOff}' % table_name
                    #'\t\t{Blue}%s{ColorOff} %s>> {BGreen}Done{ColorOff}' % (table_name, (' ' * count_spaces))
                ))

                bar()
                time.sleep(0.3)
