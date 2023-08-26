from peewee import IntegerField, TextField, ForeignKeyField
from database.connector import BaseModel
from database.model.store_model import Store
from database.model.category_model import Category


class Statistic(BaseModel):
    store = ForeignKeyField(Store)
    category = ForeignKeyField(Category)
    last_product_ean = TextField()
    num_paginator_page = IntegerField()
    status = TextField()

    class Meta:
        indexes = (
            (('store', 'category'), True),
        )
