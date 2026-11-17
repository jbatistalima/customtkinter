from app.views.pages.base_page  import BasePage
import customtkinter as ctk
from tkinter import messagebox, ttk
from app.models.category import Category


class CategoriesPage(BasePage):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)


        self.title_label = ctk.CTkLabel(self, text="Gerenciar Categorias", font=("Arial", 18))
        self.title_label.pack(pady=20)

        # Formulário para cadastrar nova categoria
        self.form_frame = ctk.CTkFrame(self)
        self.form_frame.pack(padx=10, pady=10, fill="x")

        self.form_title = ctk.CTkLabel(self.form_frame, text="Cadastrar Nova Categoria", font=("Arial", 18, "bold"))
        self.form_title.pack(padx=(10, 350), pady=10)
        
        self.entry_name = ctk.CTkEntry(self.form_frame, placeholder_text="Nome da categoria")
        self.entry_name.pack(padx=10, pady=(0, 5), fill="x")

        self.entry_description = ctk.CTkEntry(self.form_frame, placeholder_text="Descrição (opcional)")
        self.entry_description.pack(padx=10, pady=5, fill="x")

        self.btn_add = ctk.CTkButton(self.form_frame, fg_color=("#34648B", "teal"), text="Adicionar categoria", command=self.add_category)   
        self.btn_add.pack(padx=10, pady=10, fill="x")

        btn_delete = ctk.CTkButton(self.form_frame, text="Excluir", width=60, fg_color="#8f1309", command=self.delete_selected)
        btn_delete.pack(padx=10, pady=(5, 10), fill="x")

        btn_edit = ctk.CTkButton(self.form_frame, fg_color=("#34648B", "teal"), text="Editar", width=60, command=self.edit_selected)
        btn_edit.pack(padx=10, pady=(5, 10), fill="x")
        
        btn_pdf = ctk.CTkButton(self.form_frame, fg_color=("#34648B", "teal"), text="Gerar PDF", width=60, command=self.gerar_pdf_categorias)
        btn_pdf.pack(padx=10, pady=(5, 10), fill="x")

        # Frame listagem de categoria
        # --- Estilo ---
        style = ttk.Style()
        # Define a altura de cada linha(o padrão costuma ser 20)
        style.configure("Custom.Treeview", font=('Arial', 10), rowheight=35)

        # Se quiser que o cabeçalho também mude:
        style.configure("Treeview.Heading", foreground="#000000", font=('Arial', 12, 'bold')) 
        
        # Tabela de produtos
        self.tree = ttk.Treeview(self, columns=("categoria", "descricao"), show="headings", style="Custom.Treeview")
        self.tree.heading("categoria", text="Categoria", anchor="w")
        self.tree.heading("descricao", text="Descrição", anchor="w")
                
        self.tree.column("categoria", width=100, anchor="w")
        self.tree.column("descricao", width=35, anchor="w")
        
        self.tree.pack(padx=15, pady=5, fill="both", expand=True)
        self.refresh_list() 
        


    def add_category(self):
       name = self.entry_name.get().strip()
       description = self.entry_description.get().strip()

       if not name:
           messagebox.showwarning("ATENÇÃO", "É obrigatório o nome da categoria")
           return
       
       if Category.select().where(Category.name == name).exists():
           messagebox.showerror("ERRO", "Categoria já existe no cadastro!")
           return

       Category.create(name = name, description = description or None)
       messagebox.showinfo("SUCESSO", "Categoria cadastrada com sucesso!")
       self.entry_name.delete(0, "end")
       self.entry_description.delete(0, "end")
       self.refresh_list()


    def refresh_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        categories = Category.select().order_by(Category.create_at.desc())
        for i, category in enumerate(categories):
            tag = "par" if i % 2 == 0 else "impar"
            self.tree.insert("", "end", iid=category.id, values=(
            category.name,
            category.description if category.description else ""),text=category.name, tags=(tag,))
            self.tree.tag_configure("par", background="#979797")
            self.tree.tag_configure("impar", background="#808080")    
            

    def edit_category(self, category):
        window = ctk.CTkToplevel(self)
        window.title("Editar Fornecedor")
        window.geometry("500x350+400+20")
        window.resizable(False, False)
        window.transient(self) # Vincula a janela window à principal
        window.grab_set()      # Torna a janela window modal
        window.focus_force()   # Coloca o foco na janela window
        window.grid_columnconfigure(0, weight=1)
        window.grid_columnconfigure(1, weight=2)

        ctk.CTkLabel(window, text="Categoria").grid(row=0, column=0, padx=(50, 0), sticky="w")
        entry_name = ctk.CTkEntry(window)
        entry_name.insert(0, category.name)
        entry_name.grid(row=0, column=1, padx=(0,  50), pady=10, sticky="ew")
        
        ctk.CTkLabel(window, text="Descrição").grid(row=2, column=0, padx=(50, 0), sticky="w")
        entry_description = ctk.CTkEntry(window)
        entry_description.insert(0, category.description or "")
        entry_description.grid(row=2, column=1, padx=(0,  50), pady=10, sticky="ew")           


        def salvar():
            try:
                category.name = entry_name.get().strip()                
                category.description = entry_description.get().strip()
                category.save()
                self.refresh_list()
                window.destroy()
                messagebox.showinfo("Sucesso", "Categoria atualizada com sucesso!")
            except ValueError:
                messagebox.showerror("Erro", "A categoria é obrigatória.")
        ctk.CTkButton(window, text="Salvar", command=salvar).grid(row=6, column=1, padx=(0,  50), pady=15, stick="ew")
        

    def edit_selected(self):
        selected = self.tree.selection()
        
        if not selected:
            messagebox.showwarning("Aviso", "Selecione uma categoria.")
            return
        
        category = Category.get_by_id(int(selected[0]))
        self.edit_category(category)
        self.refresh_list()

            
    def delete_selected(self):
        selected = self.tree.selection()
        
        if not selected:
            messagebox.showwarning("Aviso", "Selecione uma categoria.")
            return
        category = Category.get_by_id(int(selected[0]))
        self.delete_category(category)    
        self.refresh_list()


    def delete_category(self, category):
        confirm = messagebox.askyesno("Confirmar exclusão", f"Deseja excluir a categoria {category.name}?")
        if confirm:
            category.delete_instance()
            self.refresh_list()
    
        
    def gerar_pdf_categorias(self):
        categorias = Category.select().order_by(Category.create_at.desc())
        if not categorias:
            messagebox.showwarning("Aviso", "Não há categorias cadastradas para gerar o relatório.")
            return
        from app.utils.pdf_reports import gerar_relatorio_categorias
        nome_arquivo = gerar_relatorio_categorias(categorias)
        messagebox.showinfo("Sucesso", f"Relatório de categorias gerado com sucesso!\nArquivo: {nome_arquivo}")

    
"""
from app.views.pages.base_page  import BasePage
import customtkinter as ctk
from tkinter import messagebox
from app.models.category import Category


class CategoriesPage(BasePage):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)


        self.title_label = ctk.CTkLabel(self, text="Gerenciar Categorias", font=("Arial", 18))
        self.title_label.pack(pady=20)

        # Formulário para cadastrar nova categoria
        self.form_frame = ctk.CTkFrame(self)
        self.form_frame.pack(padx=10, pady=10, fill="x")

        self.form_title = ctk.CTkLabel(self.form_frame, text="Cadastrar Nova Categoria", font=("Arial", 18, "bold"))
        self.form_title.pack(padx=(10, 350), pady=10)
        
        self.entry_name = ctk.CTkEntry(self.form_frame, placeholder_text="Nome da categoria")
        self.entry_name.pack(padx=10, pady=(0, 5), fill="x")

        self.entry_description = ctk.CTkEntry(self.form_frame, placeholder_text="Descrição (opcional)")
        self.entry_description.pack(padx=10, pady=5, fill="x")

        self.btn_add = ctk.CTkButton(self.form_frame, text="Adicionar categoria", command=self.add_category)   
        self.btn_add.pack(padx=10, pady=10, fill="x")

        # Frame listagem de categoria
        self.list_frame = ctk.CTkScrollableFrame(self, label_text="Categorias Cadastradas")
        self.list_frame.pack(padx=10, pady=10, fill="both", expand=True)
        self.refresh_list()


    def add_category(self):
       name = self.entry_name.get().strip()
       description = self.entry_description.get().strip()

       if not name:
           messagebox.showwarning("ATENÇÃO", "É obrigatório o nome da categoria")
           return
       
       if Category.select().where(Category.name == name).exists():
           messagebox.showerror("ERRO", "Categoria já existe no cadastro!")
           return

       Category.create(name = name, description = description or None)
       messagebox.showinfo("SUCESSO", "Categoria cadastrada com sucesso!")
       self.entry_description.delete(0, "end")
       self.entry_name.delete(0, "end")
       self.refresh_list()


    def refresh_list(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()
        categories = Category.select().order_by(Category.create_at.desc())
        for category in categories:
            frame = ctk.CTkFrame(self.list_frame)
            frame.pack(padx=5, pady=5, fill="x")

            name_label = ctk.CTkLabel(frame, text=f"{category.name} - {category.description or "SEM DESCRIÇÃO"}")
            name_label.pack(side="left", padx=10)

            btn_delete = ctk.CTkButton(frame, text="Excluir", width=60, fg_color="red", command=lambda c=category:self.delete_category(c))
            btn_delete.pack(side="right", padx=5)

            btn_edit = ctk.CTkButton(frame, text="Editar", width=60, command=lambda c=category:self.edit_category(c))
            btn_edit.pack(side="right", padx=5)


    def edit_category(self, category):
        new_name = ctk.CTkInputDialog(text="Novo nome: ", title="Editar categoria").get_input()
        if new_name:
            category.name = new_name.strip()
            category.save()
            self.refresh_list()


    def delete_category(self, category):
        confirm = messagebox.askyesno("Confirmar exclusão", f"Deseja excluir a categoria {category.name}?")
        if confirm:
            category.delete_instance()
            self.refresh_list()
"""       
                                            