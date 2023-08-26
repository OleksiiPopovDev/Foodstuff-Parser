from peewee import ForeignKeyField, CharField, TextField
from database.connector import BaseModel
from database.model.store_model import Store


class Product(BaseModel):
    ean = CharField()
    store_id = ForeignKeyField(Store)
    energy = CharField(null=True)
    protein = CharField(null=True)
    fat = CharField(null=True)
    carbohydrates = CharField(null=True)
    source = TextField(null=True)
    detail_source = TextField(null=True)

    class Meta:
        indexes = (
            (('ean', 'store_id'), True),
        )
