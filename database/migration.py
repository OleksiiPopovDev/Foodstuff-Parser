from database.connector import Connector
from alive_progress import alive_bar
from view.view import View
import time
import os


class Migration(Connector):
    _dump_directory: str = 'database/dumps/'
    _tables: list[str] = ['store', 'category', 'product', 'product_detail', 'statistic']
