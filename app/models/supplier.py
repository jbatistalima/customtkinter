from peewee import CharField, TextField, DateTimeField
from datetime import datetime
from app.models import db
from app.models.user import BaseModel


class Supplier(BaseModel):
    name = CharField(max_length=255, unique=True)
    contact = CharField(max_length=50, null=True)
    email = CharField(max_length=100, null=True)
    description = TextField(null=True)
    create_at = DateTimeField(default = datetime.now)


    def __str__(self):
        return self.name