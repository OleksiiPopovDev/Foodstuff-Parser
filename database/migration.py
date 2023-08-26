from database.connector import Connector
from alive_progress import alive_bar
from view.view import View
from peewee import Model
from database.model.store_model import Store
from database.model.category_model import Category
from database.model.product_model import Product
from database.model.product_detail_model import ProductDetail
from database.model.statistic_model import Statistic
import os
import time


class Migration(Connector):
    __tables: dict[Model] = {
        'store': Store,
        'category': Category,
        'product': Product,
        'product_detail': ProductDetail,
        'statistic': Statistic
    }

    def run(self):
        if os.getenv('DB_TYPE') == 'SQLite':
            self.dump_database_if_sqlite()

        with alive_bar(len(self.__tables)) as bar:
            db = Connector.get_connection()
            for table_name in self.__tables:
                bar.title(
                    View.paint('\t\t{Yellow}Creating table{ColorOff} -> {BYellow}%s{ColorOff}' % table_name)
                )

                model = self.__tables[table_name]
                db.create_tables([model])

                print(View.paint(
                    '\t\t{Yellow}Created table {ColorOff} >> {BGreen}%s{ColorOff}' % table_name
                ))

                bar()
                time.sleep(0.3)

    @staticmethod
    def dump_database_if_sqlite():
        dump_directory: str = 'database/dumps/'
        if not os.path.exists(dump_directory):
            os.makedirs(dump_directory)

        db_file: str = 'database/%s.db' % os.getenv('DB_FILE_NAME')
        if os.path.isfile(db_file):
            os.rename(db_file, 'database/dumps/%s_%s.db' % (os.getenv('DB_FILE_NAME'), time.time()))
