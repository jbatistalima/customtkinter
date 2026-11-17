import customtkinter as ctk
from tkinter import messagebox, ttk
from app.models.user import User
from app.views.pages.base_page  import BasePage


class UsersPage(BasePage):
    def __init__(self, master, current_user, **kwargs):
        super().__init__(master, **kwargs)

        self.current_user = current_user

        self.selected_user = None
        
        if not self.current_user or self.current_user.role != "admin":
            self._show_access_denied()
            return

        self._create_widgets()
        self.refresh_list()

    def _show_access_denied(self):
        access_denied_label = ctk.CTkLabel(self, text="Acesso negado. Apenas administradores podem acessar esta página.", font=("Arial", 14, "bold"), text_color="red")
        access_denied_label.pack(pady=20)


    def _create_widgets(self):
        self.title = ctk.CTkLabel(self, text="Gerenciamento de Usuários", font=("Arial", 16, "bold"))
        self.title.pack(pady=5)

        self.form_frame = ctk.CTkScrollableFrame(self)
        self.form_frame.pack(pady=5, padx=10, fill="both", expand=True)    

        self.entry_full_name = ctk.CTkEntry(self.form_frame, placeholder_text="Nome completo")
        self.entry_full_name.pack(pady=5, padx=10, fill="x")

        self.entry_username = ctk.CTkEntry(self.form_frame, placeholder_text="Nome de usuário")
        self.entry_username.pack(pady=5, padx=10, fill="x")


        self.entry_email = ctk.CTkEntry(self.form_frame, placeholder_text="Email")
        self.entry_email.pack(pady=5, padx=10, fill="x")

        self.entry_contact = ctk.CTkEntry(self.form_frame, placeholder_text="Contato")  
        self.entry_contact.pack(pady=5, padx=10, fill="x")

        self.entry_position = ctk.CTkEntry(self.form_frame, placeholder_text="Cargo")
        self.entry_position.pack(pady=5, padx=10, fill="x")

        self.entry_password = ctk.CTkEntry(self.form_frame, placeholder_text="Senha", show="*")
        self.entry_password.pack(pady=5, padx=10, fill="x") 

        self.admin_checkbox = ctk.CTkCheckBox(self.form_frame, text="Administrador")
        self.admin_checkbox.pack(padx=10, side="left", pady=15)

        self.button_frame = ctk.CTkFrame(self.form_frame)
        self.button_frame.pack(fill="x", padx=10, pady=10)

        self.add_button = ctk.CTkButton(self.button_frame, fg_color=("#34648B", "teal"), text="Adicionar Usuário", width=100, command=self.add_user)
        self.add_button.pack(pady=15, padx=(50, 0), side="left")
        
        self.update_button = ctk.CTkButton(self.button_frame, fg_color=("#34648B", "teal"), text="Atualizar Usuário", width=100, command=self.update_user)
        self.update_button.pack(pady=15, padx=(5, 0), side="left")
        
        self.pdf_button = ctk.CTkButton(self.button_frame, fg_color=("#34648B", "teal"), text="Gerar PDF", width=100, command=self.gerar_pdf_usuarios)
        self.pdf_button.pack(pady=15, padx=(5, 0), side="left")
        
        self.delete_button = ctk.CTkButton(self.button_frame, fg_color=("#34648B", "teal"), text="Excluir Usuário", width=100, command=self.delete_user)
        self.delete_button.pack(pady=15, padx=(5, 10), side="left")

        self.table_frame = ctk.CTkFrame(self)
        self.table_frame.pack(padx=20, pady=5, fill="both", expand=True)

        self.table_frame.grid_rowconfigure(0, weight=1)
        self.table_frame.grid_columnconfigure(0, weight=1)


        self.tree = ttk.Treeview(self.table_frame, columns=("nome", "usuario", "email", "cargo", "perfil"), show="headings")

        scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.tree.yview)

        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        self.tree.heading("nome", text="Nome", anchor="w")
        self.tree.heading("usuario", text="Usuário", anchor="w")
        self.tree.heading("email", text="Email", anchor="w")
        self.tree.heading("cargo", text="Cargo", anchor="w")
        self.tree.heading("perfil", text="Perfil", anchor="w")

        self.tree.column("nome", width=200)
        self.tree.column("usuario", width=120)  
        self.tree.column("email", width=180)
        self.tree.column("cargo", width=120)
        self.tree.column("perfil", width=80)  

        self.tree.bind("<Double-1>", self.load_selected_user)
        
    def add_user(self):

        full_name = self.entry_full_name.get().strip()
        username = self.entry_username.get().strip()
        email = self.entry_email.get().strip()
        contact = self.entry_contact.get().strip()
        position = self.entry_position.get().strip()
        password = self.entry_password.get().strip()

        role = "admin" if self.admin_checkbox.get() else "user"

        if not full_name:
            messagebox.showwarning("Aviso", "Informe o nome.")
            return
        
        if User.select().where(User.username == username).exists():
            messagebox.showerror("Erro", "Nome de usuário já cadastrado.")
            return
        
        if User.select().where(User.email == email).exists():
            messagebox.showwarning("Aviso", "Email já cadastrado.")
            return

        if User.select().where(User.contact == contact).exists():
            messagebox.showwarning("Aviso", "Contato já cadastrado.")
            return

        if User.select().where(User.position == position).exists():
            messagebox.showwarning("Aviso", "Cargo já cadastrado.")
            return

        if not password:        
            messagebox.showwarning("Aviso", "Informe a senha.")
            return

        try:

            if User.select().where(User.username == username).exists():
                messagebox.showerror("Erro", "Usuário já cadastrado.")
                return

            user = User(full_name=full_name, username=username, email=email, contact=contact, position=position, role=role)

            user.set_password(password)
            user.save()

            messagebox.showinfo("Sucesso", "Usuário cadastrado.")

            self.clear_form()
            self.refresh_list()

        except Exception as e:
            messagebox.showerror("Erro", str(e))
    

    def clear_form(self):
        self.entry_full_name.delete(0, "end")
        self.entry_username.delete(0, "end")
        self.entry_email.delete(0, "end")
        self.entry_contact.delete(0, "end")
        self.entry_position.delete(0, "end")
        self.entry_password.delete(0, "end")

        self.admin_checkbox.deselect()


    def refresh_list(self):

        # for widget in self.list_frame.winfo_children():
        #     widget.destroy()
        for item in self.tree.get_children():
            self.tree.delete(item)

        users = User.select().order_by(User.full_name)

        for i, user in enumerate(users):
            tag = "par" if i % 2 == 0 else "impar"
            self.tree.insert("", "end", values=(user.full_name, user.username, user.email, user.position, user.role), tags=(tag,))
            self.tree.tag_configure("par", background="#979797")
            self.tree.tag_configure("impar", background="#808080")


    def load_selected_user(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        item = self.tree.item(selected[0])
        username = item["values"][1]
        self.selected_user = User.get(User.username == username)

        self.entry_full_name.delete(0, "end")
        self.entry_full_name.insert(0, self.selected_user.full_name)

        self.entry_username.delete(0, "end")
        self.entry_username.insert(0, self.selected_user.username)

        self.entry_email.delete(0, "end")
        self.entry_email.insert(0, self.selected_user.email)

        self.entry_contact.delete(0, "end")
        self.entry_contact.insert(0, self.selected_user.contact)

        self.entry_position.delete(0, "end")
        self.entry_position.insert(0, self.selected_user.position)

        if self.selected_user.role == "admin":
            self.admin_checkbox.select()
        else:
            self.admin_checkbox.deselect()


    def update_user(self):
        if not self.selected_user:
            messagebox.showwarning("Aviso", "Selecione um usuário para atualizar.")
            return

        full_name = self.entry_full_name.get().strip()
        username = self.entry_username.get().strip()
        email = self.entry_email.get().strip()
        contact = self.entry_contact.get().strip()
        position = self.entry_position.get().strip()
        password = self.entry_password.get().strip()

        role = "admin" if self.admin_checkbox.get() else "user"

        if not full_name:
            messagebox.showwarning("Aviso", "Informe o nome.")
            return

        try:
            user = User.get(User.id == self.selected_user.id)

            user.full_name = full_name
            user.username = username
            user.email = email
            user.contact = contact
            user.position = position
            user.role = role

            if password:
                user.set_password(password)

            user.save()

            messagebox.showinfo("Sucesso", "Usuário atualizado.")

            self.clear_form()
            self.refresh_list()

        except User.DoesNotExist:
            messagebox.showerror("Erro", "Usuário não encontrado.")         


    def delete_user(self):
        if not self.selected_user:
            messagebox.showwarning("Aviso", "Selecione um usuário para excluir.")
            return 
        resposta = messagebox.askyesno("Confirmar", f"Excluir {self.selected_user.username}?")
        if resposta:
            try:
                user = User.get(User.id == self.selected_user.id)
                user.delete_instance()
                messagebox.showinfo("Sucesso", "Usuário excluído.")
                self.clear_form()
                self.refresh_list()
            except User.DoesNotExist:
                messagebox.showerror("Erro", "Usuário não encontrado.")             


    def gerar_pdf_usuarios(self):
        users = User.select().order_by(User.full_name)
        if not users:
            messagebox.showwarning("Aviso", "Não há usuários cadastrados para gerar o relatório.")
            return
        from app.utils.pdf_reports import gerar_relatorio_usuarios
        nome_arquivo = gerar_relatorio_usuarios(users)
        messagebox.showinfo("Sucesso", f"Relatório de usuários gerado com sucesso!\nArquivo: {nome_arquivo}")            