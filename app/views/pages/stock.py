import customtkinter as ctk
from app.views.pages.base_page  import BasePage
from tkinter import messagebox, ttk
from app.models.product import Product
from app.models.movement import Movement
from app.models.user import User
from app.utils.pdf_reports import gerar_relatorio_movimentos



class StockPage(BasePage):
    def __init__(self, master, user: User, **kwargs):
        super().__init__(master, **kwargs)
        self.user = user

        self.label_title = ctk.CTkLabel(self, text="Controle de Estoque", font=("Arial", 18))
        self.label_title.pack(pady=10)

        # --- Formulário ---
        self.form_frame = ctk.CTkFrame(self)
        self.form_frame.pack(pady=10, padx=10, fill="x")

        # Combobox de Produto
        self.product_options = [p.name for p in Product.select()]
        self.combo_product = ctk.CTkOptionMenu(self.form_frame, fg_color=("#34648B", "teal"), values=self.product_options or ["Nenhum"])
        self.combo_product.pack(pady=(10, 5), padx=10, fill="x")

        # Tipo de movimento
        self.combo_type = ctk.CTkOptionMenu(self.form_frame, fg_color=("#34648B", "teal"), values=["Entrada", "Saída"])
        self.combo_type.pack(pady=5, padx=10, fill="x")

        self.entry_amount = ctk.CTkEntry(self.form_frame, placeholder_text="Quantidade")
        self.entry_amount.pack(pady=5, padx=10, fill="x")

        self.entry_observation = ctk.CTkEntry(self.form_frame, placeholder_text="Observação (opcional)")
        self.entry_observation.pack(pady=5, padx=10, fill="x")

        self.btn_add = ctk.CTkButton(self.form_frame, fg_color=("#34648B", "teal"), text="Registrar Movimento", command=self.add_movement)
        self.btn_add.pack(pady=10, padx=10, fill="x")

        btn_pdf = ctk.CTkButton(self.form_frame, fg_color=("#34648B", "teal"), text="Gerar PDF", command=self.exportar_pdf)
        btn_pdf.pack(pady=10, padx=10, fill="x")
        
        # --- Histórico ---
        style = ttk.Style()
        # Define a altura de cada linha(o padrão costuma ser 20)
        style.configure("Custom.Treeview", font=('Arial', 10), rowheight=35)

        # Se quiser que o cabeçalho também mude:
        style.configure("Treeview.Heading", foreground="#000000", font=('Arial', 12, 'bold')) 
        
        # Tabela de produtos
        self.tree = ttk.Treeview(self, columns=("produto", "acao", "qtde", "data", "obs", "usuario"), show="headings", style="Custom.Treeview")
        self.tree.heading("produto", text="Produto", anchor="w")
        self.tree.heading("acao", text="Ação", anchor="w")
        self.tree.heading("qtde", text="Qtde", anchor="w")
        self.tree.heading("data", text="Data", anchor="w")
        self.tree.heading("obs", text="Obs", anchor="w")
        self.tree.heading("usuario", text="Usuário", anchor="w")
        
        self.tree.column("produto", width=100, anchor="w")
        self.tree.column("acao", width=35, anchor="w")
        self.tree.column("qtde", width=15, anchor="w")
        self.tree.column("data", width=35, anchor="w")
        self.tree.column("obs", width=175, anchor="w")
        self.tree.column("usuario", width=30, anchor="w")
        self.tree.pack(padx=15, pady=5, fill="both", expand=True)
        self.refresh_list() 


    def add_movement(self):
        product_name = self.combo_product.get()
        type_movement = self.combo_type.get().lower()
        amount = self.entry_amount.get().strip()
        observation = self.entry_observation.get().strip()

        if product_name == "":
            messagebox.showwarning("Atenção", "Selecione um produto")
            return

        try:
            product = Product.get(Product.name == product_name)
        except Product.DoesNotExists:
            messagebox.showerror("Erro", "Produto inválido!")
            return

        try:
            amount = int(amount)
            if amount <= 0:
                messagebox.showerror("Erro", "A quantidade deve ser maior que zero!")
                self.entry_amount.delete(0, "end")
                self.entry_observation.delete(0, "end")
                return
        except ValueError:
            messagebox.showerror("Erro", "A qauntidade de produto de ser numérica!")
            return

        if type_movement == "saida" or type_movement == "saída":
            if amount > product.amount:
                messagebox.showerror("Erro", f"Quantidade insufuciente! Estoque atual: {product.amount}")
                return
                
            product.amount -= amount
        elif type_movement == "entrada":
            product.amount += amount
        else:
            messagebox.showerror("Erro", "Tipo de movimentação inválida!")
        product.save()
        messagebox.showinfo("Sucesso", "Movimento registrado!")

        Movement.create(
            product=product,
            movement_type=type_movement,
            amount=amount,
            observation=observation,
            user=self.user
        )
        self.entry_amount.delete(0, "end")
        self.entry_observation.delete(0, "end")
        self.refresh_list()


    def refresh_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        movements = Movement.select().order_by(Movement.date.desc())

        for i, movement in enumerate(movements):
            tag = "par" if i % 2 == 0 else "impar"
            self.tree.insert("", "end", iid=movement.id, values=(
            movement.product,
            movement.movement_type,
            movement.amount,
            movement.date.strftime('%d/%m/%Y %H:%M'),
            movement.observation,
            movement.user),text=movement.product, tags=(tag,))
            self.tree.tag_configure("par", background="#979797")
            self.tree.tag_configure("impar", background="#808080")


    def exportar_pdf(self):

        movimentos = (Movement.select().order_by(Movement.date.desc()))

        arquivo = gerar_relatorio_movimentos(
        movimentos
        )

        messagebox.showinfo("Sucesso", f"PDF gerado:\n{arquivo}")



"""
import customtkinter as ctk
from app.views.pages.base_page  import BasePage
from tkinter import messagebox
from app.models.product import Product
from app.models.movement import Movement
from app.models.user import User


class StockPage(BasePage):
    def __init__(self, master, user: User, **kwargs):
        super().__init__(master, **kwargs)
        self.user = user

        self.label_title = ctk.CTkLabel(self, text="Controle de Estoque", font=("Arial", 18))
        self.label_title.pack(pady=10)

        # --- Formulário ---
        self.form_frame = ctk.CTkFrame(self)
        self.form_frame.pack(pady=10, padx=10, fill="x")

        # Combobox de Produto
        self.product_options = [p.name for p in Product.select()]
        self.combo_product = ctk.CTkOptionMenu(self.form_frame, values=self.product_options or ["Nenhum"])
        self.combo_product.pack(pady=(10, 5), padx=10, fill="x")

        # Tipo de movimento
        self.combo_type = ctk.CTkOptionMenu(self.form_frame, values=["entrada", "saida"])
        self.combo_type.pack(pady=5, padx=10, fill="x")

        self.entry_amount = ctk.CTkEntry(self.form_frame, placeholder_text="Quantidade")
        self.entry_amount.pack(pady=5, padx=10, fill="x")

        self.entry_observation = ctk.CTkEntry(self.form_frame, placeholder_text="Observação (opcional)")
        self.entry_observation.pack(pady=5, padx=10, fill="x")

        self.btn_add = ctk.CTkButton(self.form_frame, text="Registrar Movimento", command=self.add_movement)
        self.btn_add.pack(pady=10, padx=10, fill="x")

        # --- Histórico ---
        self.list_frame = ctk.CTkScrollableFrame(self, label_text="Histórico de Movimentos")
        self.list_frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.refresh_list()


    def add_movement(self):
        product_name = self.combo_product.get()
        type_movement = self.combo_type.get()
        amount = self.entry_amount.get().strip()
        obervation = self.entry_observation.get().strip()

        if product_name == "":
            messagebox.showwarning("Atenção", "Selecione um produto")
            return

        try:
            product = Product.get(Product.name == product_name)
        except Product.DoesNotExixsts:
            messagebox.showerror("Erro", "Produto inválido!")
            return

        try:
            amount = int(amount)
        except ValueError:
            messagebox.showerror("Erro", "A qauntidade de produto de ser numérica!")
            return

        if type_movement == "saida" and amount > product.amount:
            messagebox.showerror("Erro", "Quantidade insuficiente no estoque!")
            return

        if type_movement == "entrada":
            product.amount += amount
        else:
            product.amount -= amount
        product.save()

        Movement.create(
            product=product,
            movement_type=type_movement,
            amount=amount,
            observation=observation,
            user=self.user
        )
        messagebox.showinfo("Sucesso", "Movimento registrado!")
        self.entry_amount.delete(0, "end")
        self.entry_observation.delete(0, "end")
        self.refresh_list()


    def refresh_list(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        movements = Movement.select().order_by(Movement.date.desc())

        for movement in movements:
            frame = ctk.CTkFrame(self.list_frame)
            frame.pack(pady=5, padx=5, fill="x")

            text = f"{movement.date.strftime('%d/%m/%Y %H:%M')} - {movement.movement_type.upper()} - {movement.product.name} ({movement.amount}) - {movement.user.username}"
            lbl = ctk.CTkLabel(frame, text=text)
            lbl.pack(side="left", padx=10)
"""    