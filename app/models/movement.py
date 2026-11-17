from peewee import ForeignKeyField, IntegerField, TextField, DateTimeField, CharField
from datetime import datetime
from app.models import db
from app.models.user import BaseModel, User
from app.models.product import Product


class Movement(BaseModel):
    product = ForeignKeyField(Product, backref="movement", on_delete="CASCADE")
    movement_type = CharField(max_length=10)
    amount = IntegerField()
    observation = TextField(null=True)
    date = DateTimeField(default=datetime.now)
    user = ForeignKeyField(User, backref="movement")


    def __str__(self):
        return f"{self.movement_type} - {self.product.name} - ({self.amount})"