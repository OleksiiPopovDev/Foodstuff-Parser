from peewee import CharField, TextField
from database.connector import BaseModel


class ProductDetail(BaseModel):
    ean = CharField()
    language = CharField()
    title = TextField()
    description = TextField(null=True)
    source = TextField(null=True)

    class Meta:
        legacy_table_names = False
        indexes = (
            (('ean', 'language'), True),
        )
