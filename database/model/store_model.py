from peewee import IntegerField, CharField, TextField
from database.connector import BaseModel


class Store(BaseModel):
    id = IntegerField(primary_key=True, unique=True)
    name = CharField()
    source = TextField()
