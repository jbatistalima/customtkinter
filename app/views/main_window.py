import customtkinter as ctk
from app.views.pages.dashboard import DashboardPage
from app.views.pages.categories import CategoriesPage
from app.views.pages.products import ProductsPage
from app.views.pages.stock import StockPage
from app.views.pages.supplies import SuppliesPage
from app.views.pages.users import UsersPage


class MainWindow(ctk. CTk):
    def __init__(self, user):
        super().__init__()

        self.user = user

        self.title(f"Sistema Gestão de Estoque - Usuário logado: {self.user.username}")
        self.geometry("900x640+400+20")
        self.protocol("WM_DELETE_WINDOW", self.logout)

        ctk.set_appearance_mode("dark") # system, dark, light
        ctk.set_default_color_theme("blue") # darkblue, green, blue

        # Layout: menu lateral (frame esquerdo) + conteúdo (frame esquerdo)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # -------------------- Menu Lateral --------------------------
        self.menu_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.menu_frame.grid(row=0, column=0, stick="nsew")
        #self.menu_frame.grid.rowconfigure(7, weight=1)

        ctk.CTkLabel(self.menu_frame, text="Menu", font=("Arial", 16, "bold")).pack(pady=20)

        self.create_menu_buttons()
        
        # -------------------- área de conteúdo ----------------------
        self.content_frame = ctk.CTkFrame(self, corner_radius=0)
        self.content_frame.grid(row=0, column=1, stick="nsew")

        # Página inicial / página atual
        self.current_page = None
        self.show_page(DashboardPage)


    def create_menu_buttons(self):
        buttons = [
            ("Painel", DashboardPage),
            ("Produtos", ProductsPage),
            ("Estoque", StockPage),
            ("Categoria", CategoriesPage),
            ("Fornecedores", SuppliesPage),
        ]
        if self.user.role == "admin":
            buttons.append(("Usuários", UsersPage))
        

    # def create_menu_buttons(self):
    #     buttons = [
    #         ("Painel", DasboardPage),
    #         ("Produtos", ProductsPage),
    #         ("Estoque", StockPage),
    #         ("Categoria", CategoriesPage),
    #         ("Fornecedores", SuppliesPage),
    #     ]
    #     if self.user.role == "admin":
    #         buttons.append(("Usuários", UsersPage))

        for text, page in buttons:
            btn = ctk.CTkButton(
                self.menu_frame,
                fg_color=("#34648B", "teal"),
                text = text,
                width=180,
                command=lambda p=page: self.show_page(p)
            )     
            btn.pack(pady=5, padx=10)

        # Tema
        self.current_theme = "Dark"
        btn_theme = ctk.CTkButton(self.menu_frame, fg_color=("#34648B", "teal"), width=180, text="Alterar Tema", command=self.toggle_theme)
        btn_theme.pack(pady=5, padx=10)
        
        btn_sair = ctk.CTkButton(self.menu_frame, fg_color=("#34648B", "teal"), width=180, text="Sair", command=self.logout)
        btn_sair.pack(pady=5, padx=10)


    def show_page(self, page_class):
        """Remover a página atual e mostrar a nova página""" 
        if self.current_page:
            self.current_page.destroy() 
            self.update_idletasks()
        if page_class in (ProductsPage, StockPage, UsersPage):
            self.current_page = page_class(self.content_frame, self.user)
        else:        
            self.current_page = page_class(self.content_frame)  
        self.current_page.pack(fill="both", expand=True) 


    def toggle_theme(self):
        if self.current_theme == "Dark":
            self.current_theme = "Light"
        else: 
            self.current_theme = "Dark"
        ctk.set_appearance_mode(self.current_theme)


    def logout(self):
        from app.views.login import LoginWindow
        self.quit()
        self.destroy()

        login_window = LoginWindow()
        login_window.mainloop() 

