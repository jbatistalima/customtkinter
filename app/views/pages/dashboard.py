import customtkinter as ctk
from app.views.pages.base_page import BasePage
from app.models.product import Product
from app.models.category import Category
from app.models.supplier import Supplier
from app.models.movement import Movement
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


class DashboardPage(BasePage):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)


        label = ctk.CTkLabel(self, text="Dashboard do Sistema", font=("Arial", 18))
        label.pack(pady=20)

        # ------ Estatisticas Rapidas --------
        self.stats_frame = ctk.CTkFrame(self)
        self.stats_frame.pack(pady=10, padx=10, fill="x")

        total_products = Product.select().count()
        total_categories = Category.select().count()
        total_suppliers = Supplier.select().count()
        total_value = sum(p.amount * p.unity_purchase_price for p in Product.select())

        # -------- Cards ---------
        self._create_start_card(self.stats_frame, "Produtos", total_products, 0, "#2563EB")
        self._create_start_card(self.stats_frame, "Categorias", total_categories, 1, "#16A34A")
        self._create_start_card(self.stats_frame, "Fornecedores", total_suppliers, 2, "#EA580C")
        self._create_start_card(self.stats_frame, "Valor total do Estoque", f"R${total_value:.2f}", 3, "#7C3AED")

        # ------ Grafico --------
        self.chart_frame = ctk.CTkFrame(self)
        self.chart_frame.pack(pady=(10, 40), padx=10, fill="both", expand=True)

        self._create_stock_chart()

        # ------ Últimos movimentos --------
        self.movements_frame = ctk.CTkScrollableFrame(self)
        self.movements_frame.pack(pady=10, padx=10, fill="x")

        ctk.CTkLabel(self.movements_frame, text="Últimos movimentos", font=("Arial", 14)).pack(pady=5)

        self._show_last_movements()


    def _create_start_card(self, parent, title, value, column, color):
        frame = ctk.CTkFrame(parent, corner_radius=10, fg_color=color)
        frame.grid(row=0, column=column, padx=10, pady=8)

        ctk.CTkLabel(frame, width=302, text=title, font=("Arial", 12, "bold")).pack(pady=5)
        ctk.CTkLabel(frame, width=302, text=str(value), font=("Arial", 14, "bold")).pack(pady=5)

        parent.grid_columnconfigure(column, weight=1)  


    def _create_stock_chart(self):
        products = Product.select()
        labels = [p.name for p in products][:8]
        values = [p.amount for p in products][:8]

        if not products:
            ctk.CTkLabel(self.chart_frame, text="Sem dados de estoque para exibir!").pack()
            return

        fig, ax = plt.subplots(figsize=(5, 3))
        ax.bar(labels, values, color=("#399DAE"))
        ax.set_title("Estoque por produto")
        ax.set_ylabel("Quantidades")
        plt.setp(ax.get_xticklabels(), rotation=15, ha="right")
        fig.tight_layout()
    
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        plt.close(fig)


    def _show_last_movements(self):
        last_movements = Movement.select().order_by(Movement.date.desc()) #.limit(3)

        if not last_movements:
            ctk.CTkLabel(self.movements_frame, text="Nenhum movimento registrado!").pack()
            return
        
        texto = "  Data             Movimento     Produto              Quantidade"
        ctk.CTkLabel(self.movements_frame, text=texto, font=("Courier New", 14, "bold")).pack(anchor="w")
        for mov in last_movements:
            text = (
                f"{mov.date.strftime('%d/%m/%Y %H:%M'):25}"
                f"{mov.movement_type.upper():15}"
                f"{mov.product.name:25}"
                f"{mov.amount:>7}"
            )
            ctk.CTkLabel(self.movements_frame, text=text, font=("Courier New", 12)).pack(anchor="w")

