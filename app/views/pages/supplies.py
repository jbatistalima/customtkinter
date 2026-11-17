from app.views.pages.base_page  import BasePage
import customtkinter as ctk
from tkinter import messagebox, ttk
from app.models.supplier import Supplier
from app.utils.pdf_reports import gerar_relatorio_fornecedores


class SuppliesPage(BasePage):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)


        label = ctk.CTkLabel(self, text="Fornecedores de produtos", font=("Arial", 18))
        label.pack(pady=10) 

        # Frame do formulário
        self.form_frame = ctk.CTkFrame(self)
        self.form_frame.pack(padx=10, pady=10, fill="x")

        self.entry_name = ctk.CTkEntry(self.form_frame, placeholder_text="Nome do fornecedor (obrigatório)")
        self.entry_name.pack(padx=10, pady=10, fill="x")

        self.entry_contact = ctk.CTkEntry(self.form_frame, placeholder_text="Contato do fornecedor (opcional)")
        self.entry_contact.pack(padx=10, pady=(10, 5), fill="x")

        self.entry_email = ctk.CTkEntry(self.form_frame, placeholder_text="Email do fornecedor (opcional)")
        self.entry_email.pack(padx=10, pady=10, fill="x")

        self.entry_description = ctk.CTkEntry(self.form_frame, placeholder_text="Descrição do fornecedor (opcional)")
        self.entry_description.pack(padx=10, pady=10, fill="x")

        self.btn_add = ctk.CTkButton(self.form_frame, fg_color=("#34648B", "teal"), text="Adicionar Fornecedor", command=self.add_supplier)
        self.btn_add.pack(padx=10, pady=(5, 10), fill="x")

        btn_delete = ctk.CTkButton(self.form_frame, text="Excluir", width=60, fg_color="#8f1309", command=self.delete_selected)
        btn_delete.pack(padx=10, pady=(5, 10), fill="x")   

        btn_edit = ctk.CTkButton(self.form_frame, fg_color=("#34648B", "teal"), text="Editar", width=60, command=self.edit_selected)
        btn_edit.pack(padx=10, pady=(5, 10), fill="x")
        
        btn_pdf = ctk.CTkButton(self.form_frame, fg_color=("#34648B", "teal"), text="Gerar PDF", width=60, command=self.gerar_pdf_fornecedores)
        btn_pdf.pack(padx=10, pady=(5, 10), fill="x")

        style = ttk.Style()
        # Define a altura de cada linha(o padrão costuma ser 20)
        style.configure("Custom.Treeview", font=('Arial', 10), rowheight=35)

        # Se quiser que o cabeçalho também mude:
        style.configure("Treeview.Heading", font=('Arial', 12, 'bold')) 
        
        # Tabela de produtos
        self.tree = ttk.Treeview(self, columns=("nome", "contato", "email", "descricao"), show="headings", style="Custom.Treeview")
        self.tree.heading("nome", text="Nome", anchor="w")
        self.tree.heading("contato", text="Contato", anchor="w")
        self.tree.heading("email", text="Email", anchor="w")
        self.tree.heading("descricao", text="Descrição", anchor="w")
        
        self.tree.column("nome", width=100, anchor="w")
        self.tree.column("contato", width=50, anchor="w")
        self.tree.column("email", width=100, anchor="w")
        self.tree.column("descricao", width=160, anchor="w")
        
        self.tree.pack(padx=10, pady=5, fill="both", expand=True)
        self.refresh_list() # Carrega a lista de fornecedores


    def add_supplier(self):
        name = self.entry_name.get().strip()
        contact = self.entry_contact.get().strip()
        email = self.entry_email.get().strip()
        description = self.entry_description.get().strip()

        if not name:
            messagebox.showwarning("ATENÇÃO", "Necessário nome do fornecedor!")
            return
        if Supplier.select().where(Supplier.name == name).exists():
            messagebox.showerror("ERRO", "Fornecedor já cadastrado!")
            return
        Supplier.create(
            name = name,
            contact = contact or None,
            email = email or None,
            description = description or None
        )
        messagebox.showinfo("SUCESSO", "Fornecedor cadastrado com sucesso!")
        self.clear_form()
        self.refresh_list()


    def clear_form(self):
        self.entry_name.delete(0, "end")    
        self.entry_contact.delete(0, "end")    
        self.entry_email.delete(0, "end")    
        self.entry_description.delete(0, "end") 


    def refresh_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)       
        suppliers = Supplier.select().order_by(Supplier.create_at.desc())
        for i, supplier in enumerate(suppliers):
            tag = "par" if i % 2 == 0 else "impar"
            self.tree.insert("", "end", iid=supplier.id, values=(
            supplier.name,
            supplier.contact if supplier.contact else "",
            supplier.email if supplier.email else "",
            supplier.description if supplier.description else ""), tags=(tag,))
            self.tree.tag_configure("par", background="#979797")
            self.tree.tag_configure("impar", background="#808080")


    def edit_supplier(self, supplier):
        window = ctk.CTkToplevel(self)
        window.title("Editar Fornecedor")
        window.geometry("500x350+400+20")
        window.resizable(False, False)
        window.transient(self) # Vincula a janela window à principal
        window.grab_set()      # Torna a janela window modal
        window.focus_force()   # Coloca o foco na janela window
        window.grid_columnconfigure(0, weight=1)
        window.grid_columnconfigure(1, weight=2)
        ctk.CTkLabel(window, text="Nome").grid(row=0, column=0, padx=(50, 0), sticky="w")
        entry_name = ctk.CTkEntry(window)
        entry_name.insert(0, supplier.name)
        entry_name.grid(row=0, column=1, padx=(0,  50), pady=10, sticky="ew")
        
        ctk.CTkLabel(window, text="Contato").grid(row=1, column=0, padx=(50, 0), sticky="w")
        entry_contact = ctk.CTkEntry(window)
        entry_contact.insert(0, supplier.contact)
        entry_contact.grid(row=1, column=1, padx=(0,  50), pady=10, sticky="ew")
        
        ctk.CTkLabel(window, text="Email").grid(row=3, column=0, padx=(50, 0), sticky="w")
        entry_email = ctk.CTkEntry(window)
        entry_email.insert(0, supplier.email)
        entry_email.grid(row=3, column=1, padx=(0,  50), pady=10, sticky="ew")

        ctk.CTkLabel(window, text="Descrição").grid(row=2, column=0, padx=(50, 0), sticky="w")
        entry_description = ctk.CTkEntry(window)
        entry_description.insert(0, supplier.description or "")
        entry_description.grid(row=2, column=1, padx=(0,  50), pady=10, sticky="ew")           


        def salvar():
            try:
                supplier.name = entry_name.get().strip()
                supplier.contact = entry_contact.get().strip()
                supplier.email = entry_email.get().strip()
                supplier.description = entry_description.get().strip()
                supplier.save()
                self.refresh_list()
                window.destroy()
                messagebox.showinfo("Sucesso", "Fornecedor atualizado com sucesso!")
            except ValueError:
                messagebox.showerror("Erro", "O nome é obrigatório.")
        ctk.CTkButton(window, text="Salvar", command=salvar).grid(row=6, column=1, padx=(0,  50), pady=15, stick="ew")
        

    def edit_selected(self):
        selected = self.tree.selection()
        
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um produto.")
            return
        
        supplier = Supplier.get_by_id(int(selected[0]))
        self.edit_supplier(supplier)
        self.refresh_list()
            
    def delete_selected(self):
        selected = self.tree.selection()
        
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um produto.")
            return
        supplier = Supplier.get_by_id(int(selected[0]))
        self.delete_supplier(supplier)    
        self.refresh_list()


    def delete_supplier(self, supplier):
        confirm = messagebox.askyesno("Confirmar exclusão", f"Deseja excluir o fornecedor {supplier.name}?")
        if confirm:
            supplier.delete_instance()    
    

    def gerar_pdf_fornecedores(self):
        fornecedores = Supplier.select().order_by(Supplier.create_at.desc())
        if not fornecedores:
            messagebox.showwarning("Aviso", "Não há fornecedores cadastrados para gerar o relatório.")
            return
        nome_arquivo = gerar_relatorio_fornecedores(fornecedores)
        messagebox.showinfo("Sucesso", f"Relatório gerado com sucesso!\nArquivo: {nome_arquivo}")


"""
from app.views.pages.base_page  import BasePage
import customtkinter as ctk
from tkinter import messagebox
from app.models.supplier import Supplier

class SuppliesPage(BasePage):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)


        label = ctk.CTkLabel(self, text="Fornecedores de produtos", font=("Arial", 18))
        label.pack(pady=10) 

        # Frame do formulário
        self.form_frame = ctk.CTkFrame(self)
        self.form_frame.pack(padx=10, pady=10, fill="x")

        self.entry_name = ctk.CTkEntry(self.form_frame, placeholder_text="Nome do fornecedor (obrigatório)")
        self.entry_name.pack(padx=10, pady=10, fill="x")

        self.entry_contact = ctk.CTkEntry(self.form_frame, placeholder_text="Contato do fornecedor (opcional)")
        self.entry_contact.pack(padx=10, pady=(10, 5), fill="x")

        self.entry_email = ctk.CTkEntry(self.form_frame, placeholder_text="Email do fornecedor (opcional)")
        self.entry_email.pack(padx=10, pady=10, fill="x")

        self.entry_description = ctk.CTkEntry(self.form_frame, placeholder_text="Descrição do fornecedor (opcional)")
        self.entry_description.pack(padx=10, pady=10, fill="x")

        self.btn_add = ctk.CTkButton(self.form_frame, text="Adicionar Fornecedor", command=self.add_supplier)
        self.btn_add.pack(padx=10, pady=(5, 10), fill="x")
            
        # Frame lista de fornecedores   
        self.list_frame = ctk.CTkScrollableFrame(self, label_text="Fornecedores Cadstrados")
        self.list_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.refresh_list() # Carrega a lista de fornecedores

    def add_supplier(self):
        name = self.entry_name.get().strip()
        contact = self.entry_contact.get().strip()
        email = self.entry_email.get().strip()
        description = self.entry_description.get().strip()

        if not name:
            messagebox.showwarning("ATENÇÃO", "Necessário nome do fornecedor!")
            return
        if Supplier.select().where(Supplier.name == name).exists():
            messagebox.showerror("ERRO", "Fornecedor já cadastrado!")
            return
        Supplier.create(
            name = name,
            contact = contact or None,
            email = email or None,
            description = description or None
        )
        messagebox.showinfo("SUCESSO", "Fornecedor cadastrado com sucesso!")
        self.clear_form()
        self.refresh_list()


    def clear_form(self):
        self.entry_name.delete(0, "end")    
        self.entry_contact.delete(0, "end")    
        self.entry_email.delete(0, "end")    
        self.entry_description.delete(0, "end") 


    def refresh_list(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()       
        suppliers = Supplier.select().order_by(Supplier.create_at.desc())
        for supplier in suppliers:
            frame = ctk.CTkFrame(self.list_frame)
            frame.pack(padx=5, pady=5, fill="x") 

            label = ctk.CTkLabel(frame, text=f"{supplier.name} - {supplier.contact or ""} - {supplier.email or ""} - {supplier.description or ""}") 
            label.pack(side="left", padx=5)

            btn_delete = ctk.CTkButton(frame, text="Excluir", width=60, fg_color="red", command=lambda s=supplier:self.delete_supplier(s))
            btn_delete.pack(side="right", padx=5)   

            btn_edit = ctk.CTkButton(frame, text="Editar", width=60, command=lambda s=supplier:self.edit_supplier(s))
            btn_edit.pack(side="right", padx=5)


    def edit_supplier(self, supplier):
        new_name = ctk.CTkInputDialog(text="Novo nome: ", title="Editar categoria").get_input()
        new_contact = ctk.CTkInputDialog(text="Novo contato: ", title="Editar categoria").get_input()
        new_email = ctk.CTkInputDialog(text="Novo email: ", title="Editar categoria").get_input()
        new_description = ctk.CTkInputDialog(text="Nova descrição: ", title="Editar categoria").get_input()
        if new_name and new_contact and new_email and new_description:
            supplier.name = new_name.strip()
            supplier.contact = new_contact.strip()
            supplier.email = new_email.strip()
            supplier.description = new_description.strip()
            supplier.save()
            self.refresh_list()
    
    
    def delete_supplier(self, supplier):
        confirm = messagebox.askyesno("Confirmar exclusão", f"Deseja excluir a categoria {supplier.name}?")
        if confirm:
            supplier.delete_instance()
            self.refresh_list()
            
"""            