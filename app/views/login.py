import customtkinter as ctk
from app.models.user import User
from tkinter import messagebox


class LoginWindow(ctk.CTk):
    def __init__(self,):
        super().__init__()

        self.title("Sistema Gestão de Estoque - Login")
        self.geometry("350x250")

        ctk.set_appearance_mode("dark") # system, dark, light
        ctk.set_default_color_theme("blue") # darkblue, green, blue

        # Widgtes
        self.label_title = ctk.CTkLabel(self, text="Entrar no Sistema", font=("Arial", 18))
        self.label_title.pack(pady=20)

        self.entry_username = ctk.CTkEntry(self, placeholder_text="Nome do usuário")
        self.entry_username.pack(pady=10)

        self.entry_password = ctk.CTkEntry(self, placeholder_text="Senha do usuário", show="*")
        self.entry_password.pack(pady=10)

        self.button_login = ctk.CTkButton(self, text="Entrar", command=self.login)
        self.button_login.pack(pady=20)


    def login(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()

        if not username or not password:
            messagebox.showwarning("Atenção", "Preencha todos os campos!")
            return

        try:
            user = User.get(User.username == username)
            if user.verify_password(password):
                self.quit()
                self.destroy()  # Fecha a janela de login antes de abrir a próxima)
                from app.views.main_window import MainWindow
                main_window = MainWindow(user)
                main_window.mainloop()
            else:
                messagebox.showerror("Erro", "Senha incorreta!")
        except User.DoesNotExist:
            messagebox.showerror("Erro", "Usuário não encontrado. Solicite cadastro ou verifique usuário!")        
    
