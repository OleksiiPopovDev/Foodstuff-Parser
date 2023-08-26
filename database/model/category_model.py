from peewee import IntegerField, CharField, TextField, ForeignKeyField
from database.connector import BaseModel
from database.model.store_model import Store


class Category(BaseModel):
    page = CharField()
    store = ForeignKeyField(Store)
    product_count = IntegerField(default=0)
    source = TextField(null=True)

    class Meta:
        indexes = (
            (('page', 'store'), True),
        )
