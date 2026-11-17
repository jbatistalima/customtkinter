from peewee import (
    CharField,
    TextField,
    IntegerField,
    ForeignKeyField,
    FloatField,
    DateTimeField,
)
from datetime import datetime
from app.models.user import User, BaseModel
from app.models.category import Category
from app.models.supplier import Supplier


class Product(BaseModel):
    name = CharField(max_length=100)
    code = CharField(max_length=50, unique=True)
    category = ForeignKeyField(Category, backref="products", on_delete="CASCADE")
    supplier = ForeignKeyField(Supplier, backref="products", null=True, on_delete="SET NULL")
    description = TextField(null=True)
    amount = IntegerField(default=0)
    unity_purchase_price = FloatField(default=0.0)
    unity_sale_price = FloatField(default=0.0)
    submission_date = DateTimeField(default=datetime.now)
    submission_user = ForeignKeyField(User, backref="products")


    def __str__(self):
        return f"{self.name} ({self.code})"