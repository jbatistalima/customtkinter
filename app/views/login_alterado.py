import customtkinter as ctk
from app.models.user import User
from tkinter import messagebox
from app.views.main_window import MainWindow


class LoginWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sistema Gestão de Estoque - Login")
        self.geometry("400x300")
        self.resizable(False, False)

        ctk.set_appearance_mode("dark") # system, dark, light
        ctk.set_default_color_theme("blue") # darkblue, green, blue

        self._create_widgets() 


    def _create_widgets(self):
        title_label = ctk.CTkLabel(self, text="Sistema Gestão de Estoque", font=("Arial", 20, "bold")) 
        title_label.pack(pady=(30, 20))
                
        self.username_entry = ctk.CTkEntry(self, width=280, placeholder_text="Nome do usuário")
        self.username_entry.pack(pady=10)

        self.password_entry = ctk.CTkEntry(self, width=280, placeholder_text="Senha do usuário", show="*")
        self.password_entry.pack(pady=10)

        login_button = ctk.CTkButton(self, width=280, text="Entrar", command=self.login)
        login_button.pack(pady=20)


    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showwarning("Atenção", "Preencha todos os campos!")
            return

        try:
            user = User.get(User.username == username)
        except User.DoesNotExists:
            messagebox.showerror("Erro", "Usuário não encontrado. Solicite cadastro!")    
            return
        try:
            password_is_valid = user.verify_password(password)
        except ValueError:
            messagebox.showerror("Erro", "O hash de senha deste usuário inválido.")
            return

        if not password_is_valid:
            messagebox.showerror("Erro", "Senha incorreta.")     
            return

        self.destroy()

        main_window = MainWindow(user)
        main_window.mainloop()