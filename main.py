from app.utils.init_db import create_tables, create_admin
from app.views.login import LoginWindow


def main():
    create_tables()  # Chama a função para criar as tabelas no banco de dados
    create_admin()   # Chama a função para criar o usuário admin
    
    app = LoginWindow()
    app.mainloop()


if __name__ == "__main__":
    main() 

           