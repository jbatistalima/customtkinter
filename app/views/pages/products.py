import customtkinter as ctk
from tkinter import ttk
from tkinter import messagebox
from app.views.pages.base_page  import BasePage
from app.models.product import Product
from app.models.category import Category
from app.models.supplier import Supplier
from app.models.user import User
from app.utils.pdf_reports import gerar_relatorio_produtos



class ProductsPage(BasePage):
    def __init__(self, master, user: User, **kwargs):
        super().__init__(master, **kwargs)
        self.user = user
        
        label = ctk.CTkLabel(self, text="Gerenciar Produtos", font=("Arial", 18))
        label.pack(pady=8)    

        # Frame Formulário
        self.form_frame = ctk.CTkFrame(self)
        self.form_frame.pack(padx=10, pady=8, fill="x")

        self.entry_name = ctk.CTkEntry(self.form_frame, placeholder_text="Nome do produto")
        self.entry_name.pack(padx=10, pady=(5,8), fill="x")

        self.entry_code = ctk.CTkEntry(self.form_frame, placeholder_text="Código (SKU)")
        self.entry_code.pack(padx=10, pady=5, fill="x")

        # Combobox de categoria
        self.category_options = [c.name for c in Category.select()]
        self.combo_category = ctk.CTkOptionMenu(self.form_frame, fg_color=("#34648B", "teal"), values=self.category_options or ["Nenhuma"])
        self.combo_category.pack(padx=10, pady=5, fill="x")

        # Combobox de Fornecedor
        self.supplier_options = [supplier.name for supplier in Supplier.select()]
        self.combo_supplier = ctk.CTkOptionMenu(self.form_frame, fg_color=("#34648B", "teal"), values=self.supplier_options or ["Nenhum"])
        self.combo_supplier.pack(padx=10, pady=5, fill="x")


        self.entry_description = ctk.CTkEntry(self.form_frame, placeholder_text="Descrição (opcional)")
        self.entry_description.pack(padx=10, pady=5, fill="x")

        self.entry_amount = ctk.CTkEntry(self.form_frame, placeholder_text="Quantidade")
        self.entry_amount.pack(padx=10, pady=5, fill="x")

        self.entry_purchase_price = ctk.CTkEntry(self.form_frame, placeholder_text="Preço de compra (unidade)")
        self.entry_purchase_price.pack(padx=10, pady=5, fill="x")

        self.entry_sale_price = ctk.CTkEntry(self.form_frame, placeholder_text="Preço de venda (unidade)")
        self.entry_sale_price.pack(padx=10, pady=5, fill="x")

        self.btn_add = ctk.CTkButton(self.form_frame, fg_color=("#34648B", "teal"), text="Adicionar Produto", command=self.add_product)
        self.btn_add.pack(padx=10, pady=5, fill="x")

        btn_delete = ctk.CTkButton(self.form_frame, text="Excluir", width=60, fg_color="#8f1309", command=self.delete_selected)
        btn_delete.pack(padx=10, pady=5, fill="x")
        
        btn_edit = ctk.CTkButton(self.form_frame, fg_color=("#34648B", "teal"), text="Editar", width=60, command=self.edit_selected)
        btn_edit.pack(padx=10, pady=(5, 0), fill="x")

        btn_pdf = ctk.CTkButton(self.form_frame, fg_color=("#34648B", "teal"), text="Gerar PDF", width=60, command=self.exportar_produtos_pdf)
        btn_pdf.pack(padx=10, pady=(5, 0), fill="x")

        style = ttk.Style()
        # Define a altura de cada linha(o padrão costuma ser 20)
        style.configure("Custom.Treeview", font=('Arial', 10), rowheight=33)

        # Se quiser que o cabeçalho também mude:
        style.configure("Treeview.Heading", font=('Arial', 12, 'bold')) 

        tree_frame = ctk.CTkFrame(self)
        tree_frame.pack(padx=10, pady=5, fill="x")
        # Tabela de produtos
        self.tree = ttk.Treeview(tree_frame, columns=("codigo", "nome", "categoria", "fornecedor", "quantidade", "compra", "venda", "descricao", "usuario"), show="headings", style="Custom.Treeview")

        scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        scrollbar.pack(padx=10, side="bottom", fill="x")
        self.tree.configure(xscrollcommand=scrollbar.set)

        # Cabeçalho da lista
        self.tree.heading("codigo", text="Código", anchor="w")
        self.tree.heading("nome", text="Nome", anchor="w")
        self.tree.heading("categoria", text="Categoria", anchor="w")
        self.tree.heading("fornecedor", text="Fornecedor", anchor="w")
        self.tree.heading("quantidade", text="Qtd", anchor="w")
        self.tree.heading("compra", text="Compra", anchor="w")
        self.tree.heading("venda", text="Venda", anchor="w")
        self.tree.heading("descricao", text="Descrição", anchor="w")
        self.tree.heading("usuario", text="Usuário", anchor="w")
        # Colunas da lista
        self.tree.column("codigo", width=70, anchor="w")
        self.tree.column("nome", width=200, anchor="w")
        self.tree.column("categoria", width=150, anchor="w")
        self.tree.column("fornecedor", width=150, anchor="w")
        self.tree.column("quantidade", width=60, anchor="w")
        self.tree.column("compra", width=80, anchor="w")
        self.tree.column("venda", width=80, anchor="w")
        self.tree.column("descricao", width=300, anchor="w")
        self.tree.column("usuario", width=80, anchor="w")
        self.tree.pack(padx=10, pady=(0, 0), fill="both", expand=True)           
        
        self.refresh_list()    


    def add_product(self):
        name = self.entry_name.get().strip()
        code = self.entry_code.get().strip()
        category_name = self.combo_category.get()
        supplier_name = self.combo_supplier.get()
        description = self.entry_description.get().strip()
        amount = self.entry_amount.get().strip()
        purchase_price = self.entry_purchase_price.get().replace(",", ".")
        sale_price = self.entry_sale_price.get().replace(",", ".")

        if Product.select().where(Product.code == code).exists():
                messagebox.showerror("ERRO", "Já existe produto com esse código!")
                return

        if not name or not code:
            messagebox.showwarning("ATENÇÃO", "É obrigatório o nome e código do produto")
            return

        category = None
        if category_name and category_name != "nenhum":
            try:
                category = Category.get(Category.name == category_name)
            except Category.DoesNotExist:
                messagebox.showinfo("ERRO", "Selecione uma categoria válida!") 

        supplier = None
        if supplier_name and supplier_name != "nenhum":
            try:
                supplier = Supplier.get(Supplier.name == supplier_name)
            except Supplier.DoesNotExist:
                supplier = None
        try:
            amount = int(amount or 0)
            purchase_price = float(purchase_price or 0.0)
            sale_price = float(sale_price or 0.0)
        except ValueError:
            messagebox.showerror("ERRO", "Quantidade e preço devem serem numéricos.")                      
            return

        Product.create(
            name = name, 
            code = code,
            category = category,
            supplier = supplier,
            description = description or None,
            amount = amount,
            unity_purchase_price = purchase_price,
            unity_sale_price = sale_price,
            submission_user = self.user
        )
        messagebox.showinfo("SUCESSO", "Produto cadastrado!")
        self.clear_form()
        self.refresh_list()


    def clear_form(self):
        self.entry_name.delete(0, "end")    
        self.entry_code.delete(0, "end") 
        self.combo_category.set("Nenhuma")  # Ajustado para bater com o placeholder original   
        self.combo_supplier.set("Nenhum")   
        self.entry_description.delete(0, "end") 
        self.entry_amount.delete(0, "end")
        self.entry_purchase_price.delete(0, "end")
        self.entry_sale_price.delete(0, "end")


    def refresh_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        products = Product.select().order_by(Product.submission_date.desc())
        for i, product in enumerate(products):
            tag = "par" if i % 2 == 0 else "impar"
            self.tree.insert("", "end", iid=product.id, values=(
            product.code,
            product.name,
            product.category.name if product.category else "Nenhuma",
            product.supplier.name if product.supplier else "Nenhum",
            product.amount,
            f"R${product.unity_purchase_price:.2f}".replace(".", ","),
            f"R${product.unity_sale_price:.2f}".replace(".", ","),
            product.supplier.description if product.supplier is not None else "",
            product.submission_user),text=product.name, tags=(tag,))
            self.tree.tag_configure("par", background="#979797")
            self.tree.tag_configure("impar", background="#808080")     


    def edit_product(self, product):
        window = ctk.CTkToplevel(self)
        window.title("Editar Produto")
        window.geometry("500x450+400+20")
        window.resizable(False, False)
        window.transient(self) # Vincula a janela window à principal
        window.grab_set()      # Torna a janela window modal
        window.focus_force()   # Coloca o foco na janela window
        window.grid_columnconfigure(0, weight=1)
        window.grid_columnconfigure(1, weight=2)

        ctk.CTkLabel(window, text="Nome").grid(row=0, column=0, padx=(50, 0), sticky="w")
        entry_name = ctk.CTkEntry(window)
        entry_name.insert(0, product.name)
        entry_name.grid(row=0, column=1, padx=(0,  50), pady=10, sticky="ew")
        
        ctk.CTkLabel(window, text="Código").grid(row=1, column=0, padx=(50, 0), sticky="w")
        entry_code = ctk.CTkEntry(window)
        entry_code.insert(0, product.code)
        entry_code.grid(row=1, column=1, padx=(0,  50), pady=10, sticky="ew")
        
        
        # Combobox de categoria
        ctk.CTkLabel(window, text="Categoria").grid(row=2, column=0, padx=(50, 0), sticky="w")
        self.category_options = [c.name for c in Category.select()]
        combo_category = ctk.CTkOptionMenu(window, fg_color=("#34648B", "teal"), values=self.category_options or ["Nenhuma"])
        combo_category.grid(row=2, column=1, padx=(0, 50), pady=10, stick="ew")
        # Selacionar categoria atual
        if product.category:
            self.combo_category.set(product.category.name)

        # Combobox de Fornecedor
        ctk.CTkLabel(window, text="Fornecedor").grid(row=3, column=0, padx=(50, 0), sticky="w")
        self.supplier_options = [supplier.name for supplier in Supplier.select()]
        combo_supplier = ctk.CTkOptionMenu(window, fg_color=("#34648B", "teal"), values=self.supplier_options or ["Nenhum",])
        combo_supplier.grid(row=3, column=1, padx=(0, 50), pady=10, stick="ew")
        # Selecionar fornecedor atual
        if product.supplier:
            combo_supplier.set(product.supplier.name)
        
        ctk.CTkLabel(window, text="Descrição").grid(row=4, column=0, padx=(50, 0), sticky="w")
        entry_description = ctk.CTkEntry(window)
        entry_description.insert(0, product.description or ["Nenhum"])
        entry_description.grid(row=4, column=1, padx=(0,  50), pady=10, sticky="ew")
        
        ctk.CTkLabel(window, text="Quantidade").grid(row=5, column=0, padx=(50, 0), sticky="w")
        entry_amount = ctk.CTkEntry(window)
        entry_amount.insert(0, str(product.amount))
        entry_amount.grid(row=5, column=1, padx=(0,  50), pady=10, sticky="ew")
        
        ctk.CTkLabel(window, text="Preço Compra").grid(row=6, column=0, padx=(50, 0), sticky="w")
        entry_purchase = ctk.CTkEntry(window)
        entry_purchase.insert(0, str(product.unity_purchase_price))
        entry_purchase.grid(row=6, column=1, padx=(0,  50), pady=10, sticky="ew")
        
        ctk.CTkLabel(window, text="Preço Venda").grid(row=7, column=0, padx=(50, 0), sticky="w")
        entry_sale = ctk.CTkEntry(window)
        entry_sale.insert(0, str(product.unity_sale_price))
        entry_sale.grid(row=7, column=1, padx=(0,  50), pady=10, sticky="ew")

        
        def salvar():
            try:
                product.name = entry_name.get().strip()
                product.code = entry_code.get().strip()
                category_name = combo_category.get()
                product.category = Category.get(Category.name == category_name)
                supplier_name = combo_supplier.get()
                product.supplier = Supplier.get(Supplier.name == supplier_name)
                product.description = entry_description.get().strip()
                product.amount = int(entry_amount.get())
                product.unity_purchase_price = float(entry_purchase.get().replace(",", "."))
                product.unity_sale_price = float(entry_sale.get().replace(",", "."))

                product.save()

                self.refresh_list()
                window.destroy()
                messagebox.showinfo("Sucesso", "Produto atualizado com sucesso!")
            except ValueError:
                messagebox.showerror("Erro", "Quantidade e preços devem ser numéricos.")
        ctk.CTkButton(window, text="Salvar", command=salvar).grid(row=8, column=1, padx=(0,  50), pady=15, stick="ew")

            
                
    def edit_selected(self):
        selected = self.tree.selection()
        
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um produto.")
            return
        
        product = Product.get_by_id(int(selected[0]))
        self.edit_product(product)
        self.refresh_list()
        
    def delete_selected(self):
        selected = self.tree.selection()
        
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um produto.")
            return
        product = Product.get_by_id(int(selected[0]))
        self.delete_product(product)    
        self.refresh_list()


    def delete_product(self, product):
        confirm = messagebox.askyesno("Confirmar exclusão", f"Deseja excluir o produto {product.name}?")
        if confirm:
            product.delete_instance()
            self.refresh_list()    


    def exportar_produtos_pdf(self):

        produtos = (Product.select().order_by(Product.name))

        arquivo = gerar_relatorio_produtos(produtos)

        messagebox.showinfo("Sucesso", f"PDF gerado:\n{arquivo}")

    
"""
import customtkinter as ctk
from tkinter import messagebox
from app.views.pages.base_page  import BasePage
from app.models.product import Product
from app.models.category import Category
from app.models.supplier import Supplier
from app.models.user import User


class ProductsPage(BasePage):
    def __init__(self, master, user: User, **kwargs):
        super().__init__(master, **kwargs)
        self.user = user
        
        label = ctk.CTkLabel(self, text="Gerenciar Produtos", font=("Arial", 18))
        label.pack(pady=10)    

        # Frame Formulário
        self.form_frame = ctk.CTkFrame(self)
        self.form_frame.pack(padx=10, pady=10, fill="x")

        self.entry_name = ctk.CTkEntry(self.form_frame, placeholder_text="Nome do produto")
        self.entry_name.pack(padx=10, pady=(5,10), fill="x")

        self.entry_code = ctk.CTkEntry(self.form_frame, placeholder_text="Código (SKU)")
        self.entry_code.pack(padx=10, pady=5, fill="x")

        # Combobox de categoria
        self.category_options = [c.name for c in Category.select()]
        self.combo_category = ctk.CTkOptionMenu(self.form_frame, values=self.category_options or ["Nenhuma"])
        self.combo_category.pack(padx=10, pady=5, fill="x")

        # Combobox de Fornecedor
        self.supplier_options = [supplier.name for supplier in Supplier.select()]
        self.combo_supplier = ctk.CTkOptionMenu(self.form_frame, values=self.supplier_options or ["Nenhum"])
        self.combo_supplier.pack(padx=10, pady=5, fill="x")


        self.entry_description = ctk.CTkEntry(self.form_frame, placeholder_text="Descrição (opcional)")
        self.entry_description.pack(padx=10, pady=5, fill="x")

        self.entry_amount = ctk.CTkEntry(self.form_frame, placeholder_text="Quantidade")
        self.entry_amount.pack(padx=10, pady=5, fill="x")

        self.entry_purchase_price = ctk.CTkEntry(self.form_frame, placeholder_text="Preço de compra (unidade)")
        self.entry_purchase_price.pack(padx=10, pady=5, fill="x")

        self.entry_sale_price = ctk.CTkEntry(self.form_frame, placeholder_text="Preço de venda (unidade)")
        self.entry_sale_price.pack(padx=10, pady=5, fill="x")

        self.btn_add = ctk.CTkButton(self.form_frame, text="Adicionar Produto", command=self.add_product)
        self.btn_add.pack(padx=10, pady=10, fill="x")

        # Frame da lista
        self.list_frame = ctk.CTkScrollableFrame(self, label_text="Produtos cadastrados")
        self.list_frame.pack(padx=10, pady=10, fill="both", expand=True)
        self.refresh_list()    


    def add_product(self):
        name = self.entry_name.get().strip()
        code = self.entry_code.get().strip()
        category_name = self.combo_category.get()
        supplier_name = self.combo_supplier.get()
        description = self.entry_description.get().strip()
        amount = self.entry_amount.get().strip()
        purchase_price = self.entry_purchase_price.get().strip()
        sale_price = self.entry_sale_price.get().strip()

        if Product.select().where(Product.code == code).exists():
                messagebox.showerror("ERRO", "Já existe produto com esse código!")
                return

        if not name or not code:
            messagebox.showwarning("ATENÇÃO", "É obrigatório o nome e código do produto")
            return
        try:
            category = Category.get(Category.name == category_name)
        except Category.DoesNotExist:
            messagebox.showinfo("ERRO", "Selecione uma categoria válida!") 

        supplier = None
        if supplier_name and supplier_name != "nenhum":
            try:
                supplier = Supplier.get(Supplier.name == supplier_name)
            except Supplier.DoesNotExist:
                supplier = None
        try:
            amount = int(amount or 0)
            purchase_price = float(purchase_price or 0.0)
            sale_price = float(sale_price or 0.0)
        except ValueError:
            messagebox.showerror("ERRO", "Quantidade e preço devem serem numéricos.")                      
            return

        Product.create(
            name = name, 
            code = code,
            category = category,
            supplier = supplier,
            description = description or None,
            amount = amount,
            unity_purchase_price = purchase_price,
            unity_sale_price = sale_price,
            submission_user = self.user
        )
        messagebox.showinfo("SUCESSO", "Produto cadastrado!")
        self.clear_form()
        self.refresh_list()


    def clear_form(self):
        self.entry_name.delete(0, "end")    
        self.entry_code.delete(0, "end") 
        self.combo_category.set("Nenhuma")  # Ajustado para bater com o placeholder original   
        self.combo_supplier.set("Nenhum")   
        self.entry_description.delete(0, "end") 
        self.entry_amount.delete(0, "end")
        self.entry_purchase_price.delete(0, "end")
        self.entry_sale_price.delete(0, "end")


    def refresh_list(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()
        products = Product.select().order_by(Product.submission_date.desc())
        for product in products:
            frame = ctk.CTkFrame(self.list_frame)
            frame.pack(padx=5, pady=5, fill="x")

            name_label = ctk.CTkLabel(frame, text=f"{product.name} -=- {product.code} -=- {product.category or "Nenhuma"} -=- {product.supplier or "Nenhuma"} -=- {product.amount} -=- {product.unity_purchase_price} -=- {product.unity_sale_price} -=- {product.submission_user} ")
            name_label.pack(side="left", padx=10)

            btn_delete = ctk.CTkButton(frame, text="Excluir", width=60, fg_color="red", command=lambda p=product:self.delete_product(p))
            btn_delete.pack(side="right", padx=5)

            btn_edit = ctk.CTkButton(frame, text="Editar", width=60, command=lambda p=product:self.edit_product(p))
            btn_edit.pack(side="right", padx=5)


    def edit_product(self, product):
        new_name = ctk.CTkInputDialog(text="Novo nome: ", title="Editar produto").get_input()
        new_code = ctk.CTkInputDialog(text="Novo code: ", title="Editar categoria").get_input()
        new_category = ctk.CTkInputDialog(text="Nova categoria: ", title="Editar categoria").get_input()
        new_supplier = ctk.CTkInputDialog(text="Novo fornecedor: ", title="Editar fornecedor").get_input()
        new_description = ctk.CTkInputDialog(text="Nova descrição: ", title="Editar descrição").get_input()
        new_amount = ctk.CTkInputDialog(text="Nova quantidade: ", title="Editar quantidade").get_input()
        new_unity_purchase_price = ctk.CTkInputDialog(text="Novo preço de compra: ", title="Editar preço de compra").get_input()
        new_unity_sale_price = ctk.CTkInputDialog(text="Novo preço de venda: ", title="Editar preço de venda").get_input()
        if new_name and new_code and new_category and new_supplier and new_description and new_amount and new_unity_purchase_price and new_unity_sale_price:
            product.name = new_name.strip()
            product.code = new_code.strip()
            
            # Busca do Peewee para atualizar os relacionamentos na edição por input string
            if new_category.strip() and new_category.strip() != "Nenhuma":
                product.category = Category.get_or_none(Category.name == new_category.strip())
            else:
                product.category = None
            if new_supplier.strip() and new_supplier.strip() != "Nenhum":
                product.supplier = Supplier.get_or_none(Supplier.name == new_supplier.strip())
            else:
                product.supplier = None
            product.description = new_description.strip()
            product.amount = new_amount.strip()
            product.unity_purchase_price = new_unity_purchase_price.strip()
            product.unity_sale_price = new_unity_sale_price.strip()
            product.save()
            self.refresh_list()    


    def delete_product(self, product):
        confirm = messagebox.askyesno("Confirmar exclusão", f"Deseja excluir a categoria {product.name}?")
        if confirm:
            product.delete_instance()
            self.refresh_list()
"""        
    