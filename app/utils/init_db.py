from app.models import db
from app.models.user import User
from app.models.category import Category
from app.models.supplier import Supplier
from app.models.product import Product
from app.models.movement import Movement


def create_tables():
    with db:
        db.create_tables([User, Category, Supplier, Product, Movement, ])


if __name__ == "__main__":
    create_tables()        
    #create_admin() # Função salva em pendrive

