from app.models import db
from app.models.user import User
from app.models.category import Category
from app.models.supplier import Supplier
from app.models.product import Product
from app.models.movement import Movement


def create_tables():
    with db:
        db.create_tables([User, Category, Supplier, Product, Movement, ])

def create_admin():
    """Criar o usuario root(admin do sistema)"""
    admin_username = "admin"

    if not User.select().where(User.username == admin_username).exists():

        admin = User(
            full_name = "Usuário admin",
            username = admin_username,
            email =  "ua@email.com",
            contact = "",
            position = "Administrador",
            role = "admin"
        )
        admin.set_password("admin123")
        admin.save()
        print(f"Usuário admin criado co sucesso (user = admin  / senha = admin123)")
    else:
        print("Usuário admin já existe!")


if __name__ == "__main__":
    create_tables()        
    create_admin() # Função salva em pendrive

