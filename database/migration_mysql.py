from database.migration import Migration
from alive_progress import alive_bar
from view.view import View
import time
import os


class MigrationMySQL(Migration):
    def run(self):
        self.create_connection_mysql()

        with alive_bar(len(self._tables)) as bar:
            biggest_table_name: int = View.count_biggest_line(self._tables)

            for table_name in self._tables:
                count_spaces = View.get_count_spaces_for_line_up(table_name, biggest_table_name)
                bar.title(
                    View.paint('\t\t{Yellow}Creating table{ColorOff} -> {BYellow}%s{ColorOff}' % table_name) +
                    (' ' * count_spaces)
                )

                file = open('./migration/mysql/%s_table.db' % table_name, 'r')
                query: str = file.read()
                super().get_cursor().execute(query)
                super().commit()
                file.close()

                print(View.paint(
                    '\t\t{Yellow}Created table {ColorOff} >> {BGreen}%s{ColorOff}' % table_name
                ))

                bar()
                time.sleep(0.3)
