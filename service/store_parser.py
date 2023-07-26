import sqlite3
import time

import requests
import json
import os
from dto.store_dto import StoreDto
from alive_progress import alive_bar
from view.view import View
from repository.store_repository import StoreRepository


class StoreParser:
    _url: str = ''
    _store_list: list[StoreDto] = []
    _repository: StoreRepository = None

    def __init__(self):
        self._url = '%s/stores' % os.getenv('SOURCE_URL')
        self._repository = StoreRepository()

    def run(self):
        response = requests.get(self._url)
        store_list = response.json()
        if not isinstance(store_list, list):
            raise RuntimeError('The endpoint of Stores returned incorrect data format!')

        store_count: int = len(store_list)
        print('\t%sFound stores: %s%d%s' % (View.COLOR_YELLOW, View.COLOR_RED, store_count, View.COLOR_DEFAULT))

        with alive_bar(store_count) as bar:
            print('\t%sParsing...%s' % (View.COLOR_YELLOW, View.COLOR_DEFAULT))
            for store in store_list:
                self._store_list.append(StoreDto(
                    id=int(store['id']),
                    name=str(store['name']),
                    source=json.dumps(store)
                ))
                time.sleep(0.01)
                bar()

        with alive_bar(len(self._store_list)) as bar:
            print('\t%sSaving...%s' % (View.COLOR_YELLOW, View.COLOR_DEFAULT))
            for store in self._store_list:
                try:
                    self._repository.save(store)
                except (sqlite3.OperationalError, sqlite3.IntegrityError) as message:
                    print('\t%s%s (%s%d%s)%s Error: %s%s' % (
                        View.COLOR_BLUE,
                        store.name,
                        View.COLOR_L_BLUE,
                        store.id,
                        View.COLOR_BLUE,
                        View.COLOR_RED,
                        message,
                        View.COLOR_DEFAULT
                    ))
                bar()
